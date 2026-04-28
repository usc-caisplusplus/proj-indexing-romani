"""Stage 2: take the LLM's free-form answers and resolve them to entries
in the controlled-vocabulary choice groups using embedding-based retrieval
followed by an LLM judging step.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from .choice_groups import (
    FIELD_ALLOWS_PROPOSED,
    ChoiceGroup,
    embed_texts,
)
from .schema import (
    FamilyPerson,
    GhettoCampPrison,
    HidingLocation,
    Interviewee,
    RawIndexing,
    ResolvedFamilyPerson,
    ResolvedGhettoCampPrison,
    ResolvedHidingLocation,
    ResolvedInterviewee,
    ResolvedTerm,
)

logger = logging.getLogger(__name__)


JUDGE_SYSTEM_PROMPT = """You are matching a free-form answer extracted from \
a Holocaust survivor interview to a controlled vocabulary used by the USC \
Shoah Foundation.

You will be given:
- the field name (e.g. city_of_birth, camps, religious_identity_prewar)
- the free-form answer text (the indexer's raw extraction)
- optional surrounding context
- a numbered list of candidate vocabulary labels with their KeywordIDs

Pick exactly ONE candidate that matches, OR mark the answer as a proposed \
new term if no candidate is a clear semantic match. Be strict: if the \
candidates are merely loosely related (e.g. wrong country, wrong location \
type, generic vs specific mismatch), choose `propose`.

Special rules:
- Camp / ghetto / prison labels look like `City (Country : Type)` (e.g. \
  `Auschwitz (Poland : Concentration Camp)(generic)`). Prefer `(generic)` \
  variants when the transcript does not distinguish sub-camps.
- City labels look like `City (Country : city)`. Country labels are bare, \
  e.g. `Poland`. Use the country in effect at the relevant historical date.
- Religious identity labels are short, e.g. `Orthodox Judaism`, \
  `Reform Judaism`, `Hasidism`. Prefer the most specific match supported by \
  the text.
- If the field is `special_events`, you MUST pick a candidate (proposed new \
  terms are not allowed for this field). If none match, return \
  `none_applicable: true`.
- If the free-form text is empty, return `none_applicable: true`.

Output JSON only.
"""


JUDGE_RESPONSE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "decision": {"type": "string", "enum": ["match", "propose", "none_applicable"]},
        "keyword_id": {"type": ["integer", "null"]},
        "label": {"type": ["string", "null"]},
        "confidence": {"type": "number"},
        "notes": {"type": "string"},
    },
    "required": ["decision", "keyword_id", "label", "confidence", "notes"],
}


@dataclass
class MatcherConfig:
    extraction_model: str
    embedding_model: str
    top_k: int = 15
    judge_temperature: float = 0.0


@retry(stop=stop_after_attempt(4), wait=wait_random_exponential(min=1, max=15))
def _judge(
    client: OpenAI,
    model: str,
    field: str,
    text: str,
    context: str,
    candidates: Sequence[tuple[int, str, float]],
    allow_propose: bool,
    temperature: float,
) -> dict:
    candidate_block = "\n".join(
        f"  {i + 1}. [{kid}] {label}  (sim={score:.3f})"
        for i, (kid, label, score) in enumerate(candidates)
    )
    user_prompt = (
        f"Field: {field}\n"
        f"Free-form answer: {text!r}\n"
        f"Surrounding context: {context!r}\n"
        f"Allow proposed new term: {allow_propose}\n\n"
        f"Candidates:\n{candidate_block}\n\n"
        "Choose one match by KeywordID, or return decision='propose' (if "
        "allowed) or decision='none_applicable' (if the field truly does "
        "not apply or the text is empty)."
    )
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "MatchDecision",
                "strict": True,
                "schema": JUDGE_RESPONSE_SCHEMA,
            },
        },
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return json.loads(response.choices[0].message.content or "{}")


def _resolve_term(
    client: OpenAI,
    cfg: MatcherConfig,
    field: str,
    text: str,
    context: str,
    group: Optional[ChoiceGroup],
) -> ResolvedTerm:
    text = (text or "").strip()
    if not text or group is None:
        return ResolvedTerm(text=text)

    query_vec = embed_texts(client, cfg.embedding_model, [text])[0]
    candidates = group.search(query_vec, top_k=cfg.top_k)
    decision = _judge(
        client=client,
        model=cfg.extraction_model,
        field=field,
        text=text,
        context=context,
        candidates=candidates,
        allow_propose=FIELD_ALLOWS_PROPOSED.get(field, True),
        temperature=cfg.judge_temperature,
    )

    if decision.get("decision") == "match" and decision.get("keyword_id") is not None:
        return ResolvedTerm(
            text=text,
            keyword_id=int(decision["keyword_id"]),
            label=decision.get("label"),
            is_proposed=False,
            confidence=float(decision.get("confidence", 0.0)),
            notes=decision.get("notes", ""),
        )
    if decision.get("decision") == "none_applicable":
        return ResolvedTerm(text=text, notes=decision.get("notes", ""))

    return ResolvedTerm(
        text=text,
        is_proposed=True,
        confidence=float(decision.get("confidence", 0.0)),
        notes=decision.get("notes", ""),
    )


def _resolve_term_list(
    client: OpenAI,
    cfg: MatcherConfig,
    field: str,
    texts: List[str],
    context: str,
    group: Optional[ChoiceGroup],
) -> List[ResolvedTerm]:
    return [_resolve_term(client, cfg, field, t, context, group) for t in texts if t]


def _resolve_gcp(
    client: OpenAI,
    cfg: MatcherConfig,
    field: str,
    items: List[GhettoCampPrison],
    group: Optional[ChoiceGroup],
) -> List[ResolvedGhettoCampPrison]:
    out: List[ResolvedGhettoCampPrison] = []
    for it in items:
        text_parts = [it.name]
        if it.location_hint:
            text_parts.append(it.location_hint)
        text = " - ".join(p for p in text_parts if p)
        ctx = it.notes or it.dates
        term = _resolve_term(client, cfg, field, text, ctx, group)
        out.append(ResolvedGhettoCampPrison(term=term, dates=it.dates, notes=it.notes))
    return out


def _resolve_hiding(
    client: OpenAI,
    cfg: MatcherConfig,
    locations: List[HidingLocation],
    groups: Dict[str, ChoiceGroup],
) -> List[ResolvedHidingLocation]:
    out: List[ResolvedHidingLocation] = []
    loc_group = groups.get("hiding_location")
    type_group = groups.get("hiding_type")
    for loc in locations:
        place = _resolve_term(client, cfg, "hiding_location", loc.place, loc.notes, loc_group)
        types = _resolve_term_list(client, cfg, "hiding_type", loc.types, loc.notes, type_group)
        out.append(ResolvedHidingLocation(location=place, types=types, notes=loc.notes))
    return out


def _resolve_family(
    client: OpenAI,
    cfg: MatcherConfig,
    family: List[FamilyPerson],
    groups: Dict[str, ChoiceGroup],
) -> List[ResolvedFamilyPerson]:
    out: List[ResolvedFamilyPerson] = []
    place_group = groups.get("city_of_birth")  # used for both POB / POD lookups
    for person in family:
        pob_text = person.place_of_birth_text
        if person.place_of_birth_country and person.place_of_birth_country not in pob_text:
            pob_text = (
                f"{pob_text} ({person.place_of_birth_country})"
                if pob_text
                else person.place_of_birth_country
            )
        pod_text = person.place_of_death_text
        if person.place_of_death_country and person.place_of_death_country not in pod_text:
            pod_text = (
                f"{pod_text} ({person.place_of_death_country})"
                if pod_text
                else person.place_of_death_country
            )

        ctx = f"{person.relationship} of interviewee; {person.notes}".strip("; ")
        pob = _resolve_term(client, cfg, "city_of_birth", pob_text, ctx, place_group)
        pod = _resolve_term(client, cfg, "city_of_birth", pod_text, ctx, place_group)
        out.append(ResolvedFamilyPerson(raw=person, place_of_birth=pob, place_of_death=pod))
    return out


def resolve_indexing(
    client: OpenAI,
    cfg: MatcherConfig,
    raw: RawIndexing,
    groups: Dict[str, ChoiceGroup],
) -> ResolvedInterviewee:
    iv: Interviewee = raw.interviewee

    return ResolvedInterviewee(
        raw=iv,
        city_of_birth=_resolve_term(
            client, cfg, "city_of_birth", iv.city_of_birth, iv.country_of_birth, groups.get("city_of_birth")
        ),
        country_of_birth=_resolve_term(
            client, cfg, "country_of_birth", iv.country_of_birth, "", groups.get("country_of_birth")
        ),
        religious_identity_prewar=_resolve_term(
            client,
            cfg,
            "religious_identity_prewar",
            iv.religious_identity_prewar,
            "prewar",
            groups.get("religious_identity_prewar"),
        ),
        religious_identity_postwar=_resolve_term(
            client,
            cfg,
            "religious_identity_postwar",
            iv.religious_identity_postwar,
            "postwar",
            groups.get("religious_identity_postwar"),
        ),
        ghettos=_resolve_gcp(client, cfg, "ghettos", iv.ghettos, groups.get("ghettos")),
        camps=_resolve_gcp(client, cfg, "camps", iv.camps, groups.get("camps")),
        prisons=_resolve_gcp(client, cfg, "camps", iv.prisons, groups.get("camps")),
        hiding_locations=_resolve_hiding(client, cfg, iv.hiding.locations, groups),
        resistance_groups=_resolve_term_list(
            client, cfg, "resistance_groups", iv.resistance.groups, "", groups.get("resistance_groups")
        ),
        who_liberated=_resolve_term(
            client,
            cfg,
            "who_liberated",
            iv.liberation.who_liberated,
            iv.liberation.notes,
            groups.get("who_liberated"),
        ),
        where_liberated=_resolve_term(
            client,
            cfg,
            "where_liberated",
            iv.liberation.where_liberated,
            iv.liberation.notes,
            groups.get("where_liberated"),
        ),
        other_attributes=_resolve_term_list(
            client, cfg, "other_attributes", iv.other_attributes, "", groups.get("other_attributes")
        ),
        special_events=_resolve_term_list(
            client, cfg, "special_events", iv.special_events, "", groups.get("special_events")
        ),
    )


def resolve_family_people(
    client: OpenAI,
    cfg: MatcherConfig,
    raw: RawIndexing,
    groups: Dict[str, ChoiceGroup],
) -> List[ResolvedFamilyPerson]:
    return _resolve_family(client, cfg, raw.family_people, groups)
