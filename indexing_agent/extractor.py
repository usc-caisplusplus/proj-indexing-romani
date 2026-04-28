"""Stage 1: ask the LLM to read a transcript and produce a draft
biographical-indexing JSON document conforming to `RawIndexing`.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from .schema import RawIndexing

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are an expert biographical indexer for the USC Shoah \
Foundation Visual History Archive. Your job is to read an English Holocaust \
survivor interview transcript and extract structured biographical \
information following the official indexing guidelines (sections 2.4-2.6).

Key rules:
- Extract ONLY information that is explicitly stated in the transcript or \
  can be reasonably inferred. Never fabricate names, dates, or places.
- Use the exact date format `MMM D, YYYY` (e.g. `Jan 12, 1925`). For year-only \
  use `YYYY`; for month/year use `MMM YYYY`. Use `@ 1944` for estimated dates. \
  Use `summer 1944`, `early 1960s`, `prewar`, `wartime`, `postwar` etc. when \
  the source is non-specific.
- For unverified spelling append `*` to the name. For presumed names use \
  square brackets, e.g. `[Cohen]`.
- Survivor status (Yes/No/Unknown): apply the Holocaust survivor definition \
  from the guidelines (persecuted under Nazi/Axis control 1933-May 8 1945, \
  forced to live clandestinely, or fled). Always provide a 1-2 sentence \
  justification.
- Family/people: include EVERY person the interviewee mentions by name or \
  clear relationship (parents, siblings, spouses, children, aunts, uncles, \
  cousins, friends, rescuers, etc.). Skip people referred to only by a title \
  with no name (e.g. "the maid"). Use "baby" in the first-name field for \
  unnamed infants.
- Cause of death: only mark "Holocaust-related death" when the death is \
  explicitly attributed to the Holocaust in the transcript. Otherwise use \
  "Natural death", "Other type of death", "Interviewee does not know", or \
  "Not specified".
- For Yes/No fields (flight, hiding, resistance, forced_marches): use "Yes" \
  / "No" if clearly stated. Use "" (empty string) if the transcript is \
  silent.
- For city/country/ghetto/camp/etc. fields, write the free-form name as it \
  appears in the transcript (or the closest English form). A separate \
  matching step will resolve these to controlled-vocabulary keywords.
- For ghettos, camps, prisons: include EVERY incarceration site the \
  interviewee personally experienced. Include date ranges when given.
- For aliases: capture maiden names, name changes, anglicised names, Hebrew \
  names, false names used during the war, etc. Tag the alias_type \
  appropriately.
- Special events / situations: pick from realistic categories such as \
  "identity concealment", "displaced persons camps", "Kindertransport", \
  "camp medical experiments", "camp escapes", "forced labor", "separated \
  from family", "death marches", "ghettos", "prisons".

Output ONLY valid JSON matching the supplied schema. Do not include any \
prose, markdown, or commentary outside the JSON object.
"""


def _build_user_prompt(transcript_id: str, transcript_text: str) -> str:
    return (
        f"Transcript ID: {transcript_id}\n\n"
        "TRANSCRIPT (English; tagged with [INTERVIEWER] / [INTERVIEWEE]):\n"
        "----------------------------------------\n"
        f"{transcript_text}\n"
        "----------------------------------------\n\n"
        "Return a JSON object that conforms to the `RawIndexing` schema. "
        "Set `transcript_id` to the value above. Use empty strings or empty "
        "arrays for any field where the transcript provides no information. "
        "Use `extraction_notes` to flag any ambiguities or important "
        "uncertainties you noticed."
    )


def _strip_for_json_schema(model_schema: Dict[str, Any]) -> Dict[str, Any]:
    """Remove fields the OpenAI structured-output spec does not accept and
    enforce ``additionalProperties: false`` recursively (required by the API).

    We must distinguish between a key called ``title`` that is a JSON Schema
    *annotation* on a schema node and a key called ``title`` that is the
    *name of a property* in a ``properties`` map - we only strip the former.
    """

    def walk_schema_node(node: Any) -> None:
        if not isinstance(node, dict):
            return
        node.pop("title", None)
        node.pop("default", None)
        if node.get("type") == "object":
            node["additionalProperties"] = False
            props = node.get("properties")
            if isinstance(props, dict):
                node["required"] = list(props.keys())
                for child in props.values():
                    walk_schema_node(child)
        if "items" in node:
            walk_schema_node(node["items"])
        for combinator in ("anyOf", "oneOf", "allOf"):
            if combinator in node and isinstance(node[combinator], list):
                for child in node[combinator]:
                    walk_schema_node(child)
        if "$defs" in node and isinstance(node["$defs"], dict):
            for child in node["$defs"].values():
                walk_schema_node(child)
        if "definitions" in node and isinstance(node["definitions"], dict):
            for child in node["definitions"].values():
                walk_schema_node(child)

    walk_schema_node(model_schema)
    return model_schema


@retry(stop=stop_after_attempt(4), wait=wait_random_exponential(min=2, max=30))
def extract_indexing(
    client: OpenAI,
    model: str,
    transcript_id: str,
    transcript_text: str,
    temperature: float = 0.0,
) -> RawIndexing:
    schema = _strip_for_json_schema(RawIndexing.model_json_schema())
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "RawIndexing",
                "strict": True,
                "schema": schema,
            },
        },
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(transcript_id, transcript_text)},
        ],
    )
    raw = response.choices[0].message.content or "{}"
    data = json.loads(raw)
    data.setdefault("transcript_id", transcript_id)
    return RawIndexing.model_validate(data)
