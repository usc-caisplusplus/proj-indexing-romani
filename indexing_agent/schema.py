"""Pydantic models describing the JSON output for each transcript.

The schema mirrors the USC Shoah Foundation biographical indexing fields
(sections 2.4 - 2.6 of the guidelines).  The LLM is asked to return JSON
matching the `RawIndexing` schema; the matcher then enriches indexing-term
fields with `KeywordID` / `Label` resolved against the choice group
vocabulary (or marks them as proposed new terms).
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


YesNoUnknownBlank = Literal["Yes", "No", "Unknown", ""]
YesNoBlank = Literal["Yes", "No", ""]
GenderBlank = Literal["Male", "Female", "Unknown", ""]
CauseOfDeath = Literal[
    "Holocaust-related death",
    "Rwandan Tutsi Genocide-related death",
    "Interviewee does not know",
    "Natural death",
    "Other type of death",
    "Not specified",
    "",
]


# ---------------------------------------------------------------------------
# Raw extraction schema (what the LLM returns)
# ---------------------------------------------------------------------------


class PersonName(BaseModel):
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    title: str = ""
    notes: str = ""


class Alias(BaseModel):
    alias_type: str = Field(
        "",
        description=(
            "One of: 'Name at Birth', 'Last Name During War', "
            "'Current Last Name', 'Maiden Name', 'Presumed Name', "
            "'False Name', 'Hebrew Name', 'Other Name', 'Nickname'."
        ),
    )
    name: str = ""
    notes: str = ""


class GhettoCampPrison(BaseModel):
    name: str = Field("", description="Free-form name from transcript, e.g. 'Auschwitz'.")
    location_hint: str = Field("", description="Country / city qualifier if mentioned, e.g. 'Poland'.")
    dates: str = Field("", description="Date range if mentioned, e.g. 'Apr 1942 - Aug 1944'.")
    notes: str = ""


class HidingLocation(BaseModel):
    place: str = Field("", description="City / region where the interviewee hid.")
    types: List[str] = Field(default_factory=list, description="Types of hiding place, e.g. ['farms','convents'].")
    notes: str = ""


class FamilyPerson(BaseModel):
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    title: str = ""
    maiden_name: str = ""
    aliases: List[Alias] = Field(default_factory=list)
    gender: GenderBlank = ""
    date_of_birth: str = ""
    date_of_death: str = ""
    relationship: str = Field(
        "",
        description=(
            "Primary relationship to the interviewee, e.g. 'Father', 'Mother', "
            "'Brother', 'Sister', 'Aunt, maternal', 'Uncle', 'Cousin', "
            "'Extended family member', 'Friend', 'Aid giver'."
        ),
    )
    biological: YesNoUnknownBlank = ""
    cause_of_death: CauseOfDeath = ""
    cause_of_death_details: str = ""
    survivor_status: YesNoUnknownBlank = ""
    place_of_birth_text: str = Field("", description="Free-form text for the person's place of birth.")
    place_of_birth_country: str = ""
    place_of_death_text: str = Field("", description="Free-form text for the person's place of death.")
    place_of_death_country: str = ""
    notes: str = ""


class Liberation(BaseModel):
    who_liberated: str = Field("", description="Liberating armed force or resistance group (free text).")
    where_liberated: str = Field("", description="Location of liberation (free text).")
    date: str = ""
    notes: str = ""


class Massacre(BaseModel):
    escaped: YesNoUnknownBlank = ""
    location: str = ""
    notes: str = ""


class HidingSection(BaseModel):
    went_into_hiding: YesNoUnknownBlank = ""
    locations: List[HidingLocation] = Field(default_factory=list)
    notes: str = ""


class ResistanceSection(BaseModel):
    involved: YesNoUnknownBlank = ""
    groups: List[str] = Field(default_factory=list, description="Free-form names of resistance groups.")
    notes: str = ""


class EntryInfo(BaseModel):
    indexer_initials: str = ""
    date_of_entry: str = ""
    piq_language: List[str] = Field(default_factory=list)


class InterviewMetadata(BaseModel):
    interview_date: str = ""
    interviewer_name: str = ""
    location_of_interview: str = ""
    languages_spoken: List[str] = Field(default_factory=list)


class InterviewerStatement(BaseModel):
    summary: str = Field(
        "",
        description=(
            "1-2 sentence justification for survivor status drawn directly "
            "from the testimony (per guideline section 2.5.4)."
        ),
    )


class Interviewee(BaseModel):
    name: PersonName = Field(default_factory=PersonName)
    aliases: List[Alias] = Field(default_factory=list)
    gender: GenderBlank = ""
    date_of_birth: str = ""
    survivor_status: YesNoUnknownBlank = ""
    survivor_status_justification: str = ""
    city_of_birth: str = ""
    country_of_birth: str = ""
    religious_identity_prewar: str = ""
    religious_identity_postwar: str = ""
    flight: YesNoBlank = ""
    flight_notes: str = ""
    ghettos: List[GhettoCampPrison] = Field(default_factory=list)
    camps: List[GhettoCampPrison] = Field(default_factory=list)
    prisons: List[GhettoCampPrison] = Field(default_factory=list)
    massacres: Massacre = Field(default_factory=Massacre)
    hiding: HidingSection = Field(default_factory=HidingSection)
    resistance: ResistanceSection = Field(default_factory=ResistanceSection)
    forced_marches: YesNoBlank = ""
    forced_marches_notes: str = ""
    liberation: Liberation = Field(default_factory=Liberation)
    other_attributes: List[str] = Field(default_factory=list)
    special_events: List[str] = Field(default_factory=list)


class RawIndexing(BaseModel):
    """The free-form draft the LLM produces from the transcript."""

    transcript_id: str = ""
    entry_info: EntryInfo = Field(default_factory=EntryInfo)
    interview: InterviewMetadata = Field(default_factory=InterviewMetadata)
    interviewee: Interviewee = Field(default_factory=Interviewee)
    family_people: List[FamilyPerson] = Field(default_factory=list)
    extraction_notes: str = Field(
        "",
        description="Free-form notes from the extraction model about ambiguities or gaps.",
    )


# ---------------------------------------------------------------------------
# Resolved schema (matcher output: free-form + chosen indexing term)
# ---------------------------------------------------------------------------


class ResolvedTerm(BaseModel):
    text: str = Field("", description="Free-form text as found in transcript.")
    keyword_id: Optional[int] = Field(None, description="Matched ChoiceGroup keyword ID, if any.")
    label: Optional[str] = Field(None, description="Matched ChoiceGroup label, if any.")
    is_proposed: bool = Field(
        False,
        description="True if no good match was found and this is a proposed new term.",
    )
    confidence: Optional[float] = Field(
        None,
        description="0-1 self-reported confidence that the chosen label matches the text.",
    )
    notes: str = ""


class ResolvedGhettoCampPrison(BaseModel):
    term: ResolvedTerm = Field(default_factory=ResolvedTerm)
    dates: str = ""
    notes: str = ""


class ResolvedHidingLocation(BaseModel):
    location: ResolvedTerm = Field(default_factory=ResolvedTerm)
    types: List[ResolvedTerm] = Field(default_factory=list)
    notes: str = ""


class ResolvedFamilyPerson(BaseModel):
    raw: FamilyPerson
    place_of_birth: ResolvedTerm = Field(default_factory=ResolvedTerm)
    place_of_death: ResolvedTerm = Field(default_factory=ResolvedTerm)


class ResolvedInterviewee(BaseModel):
    raw: Interviewee
    city_of_birth: ResolvedTerm = Field(default_factory=ResolvedTerm)
    country_of_birth: ResolvedTerm = Field(default_factory=ResolvedTerm)
    religious_identity_prewar: ResolvedTerm = Field(default_factory=ResolvedTerm)
    religious_identity_postwar: ResolvedTerm = Field(default_factory=ResolvedTerm)
    ghettos: List[ResolvedGhettoCampPrison] = Field(default_factory=list)
    camps: List[ResolvedGhettoCampPrison] = Field(default_factory=list)
    prisons: List[ResolvedGhettoCampPrison] = Field(default_factory=list)
    hiding_locations: List[ResolvedHidingLocation] = Field(default_factory=list)
    resistance_groups: List[ResolvedTerm] = Field(default_factory=list)
    who_liberated: ResolvedTerm = Field(default_factory=ResolvedTerm)
    where_liberated: ResolvedTerm = Field(default_factory=ResolvedTerm)
    other_attributes: List[ResolvedTerm] = Field(default_factory=list)
    special_events: List[ResolvedTerm] = Field(default_factory=list)


class IndexingDocument(BaseModel):
    """Final output written to disk for each transcript."""

    transcript_id: str
    source_file: str
    model: str
    schema_version: str = "1.0"
    entry_info: EntryInfo = Field(default_factory=EntryInfo)
    interview: InterviewMetadata = Field(default_factory=InterviewMetadata)
    interviewee: ResolvedInterviewee
    family_people: List[ResolvedFamilyPerson] = Field(default_factory=list)
    extraction_notes: str = ""
