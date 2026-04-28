# USC Shoah Foundation Biographical Indexing Agent

An LLM + RAG pipeline that reads a Holocaust survivor interview transcript
and produces a structured JSON file conforming to the USC Shoah Foundation
biographical-indexing fields (sections 2.4 - 2.6 of the official guidelines).

For every transcript in `FHM_transcript_combined/` you get a corresponding
`output/<id>.json` with the interviewee's biographical data, every family
member / person mentioned, and indexing-term answers resolved against the
controlled vocabulary in the `Jewish survivor question choices_*.xlsx`
workbook.

---

## How it works

```
                 +-------------------------+
   transcript -->|  Stage 1: Extraction    |  one OpenAI chat-completion
                 |  (LLM, structured JSON) |  with strict JSON-schema mode
                 +-----------+-------------+
                             |
                             v
                 +-------------------------+
                 |    RawIndexing draft    |  free-form names, dates,
                 |  (per indexing fields)  |  cities, camps, etc.
                 +-----------+-------------+
                             |
                             v
                 +-------------------------+
                 |  Stage 2: RAG matching  |  for every indexing-term field:
                 |  - embed free-form text |   1) cosine search over the
                 |  - top-K candidates     |      pre-embedded choice group
                 |  - LLM judge picks one  |   2) LLM picks best match or
                 |    (or proposes new)    |      proposes a new term
                 +-----------+-------------+
                             |
                             v
                 +-------------------------+
                 |   IndexingDocument      |  written to output/<id>.json
                 +-------------------------+
```

The choice-group embeddings are computed once and cached on disk
(`.indexing_cache/`), so subsequent runs only embed transcript queries.

---

## Setup

```bash
cd "/Users/zhangyuhui/Downloads/CAIS Project"

# 1. Create / reuse the venv
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Provide an OpenAI API key
cp .env.example .env
# then edit .env and set OPENAI_API_KEY=sk-...
```

You can also export the key directly: `export OPENAI_API_KEY=sk-...`.

### Models used (defaults; override with env vars or CLI flags)

| Purpose          | Model                       | Why |
|------------------|-----------------------------|-----|
| Extraction + judging | `gpt-4o-mini`           | Cheap, fast, strong on structured-output JSON |
| Embeddings           | `text-embedding-3-small` | Cheap, plenty good for keyword retrieval |

---

## Usage

```bash
source .venv/bin/activate

# (One-time) build the choice-group embedding cache.
# Takes ~1-2 minutes and ~$0.03 in OpenAI credits the first time;
# subsequent runs reuse the cache instantly.
python -m indexing_agent.cli --build-cache-only

# Index a single transcript
python -m indexing_agent.cli --ids 53690

# Index a few transcripts
python -m indexing_agent.cli --ids 53690,53691,53692

# Index everything (resumable: skips files that already have output)
python -m indexing_agent.cli --all

# Sample run on the first 5 transcripts
python -m indexing_agent.cli --all --limit 5

# Force re-process
python -m indexing_agent.cli --ids 53690 --overwrite

# Bigger candidate pool for the judge
python -m indexing_agent.cli --ids 53690 --top-k 25

# Verbose logs
python -m indexing_agent.cli --ids 53690 -v
```

Outputs go to `output/<transcript_id>.json` by default. Override with
`--output-dir`.

### Cost ballpark

With the default models and the transcripts in this project (~207 files,
median ~11K words):

- One-time embedding cache build: **~$0.03**
- Per transcript: **~$0.005-0.02** (depends on transcript length and
  number of family members / camps / etc. needing matching)
- Full corpus (all 207): **~$1-3**

---

## Output schema

Each `output/<id>.json` is an `IndexingDocument`, sketched here:

```json
{
  "transcript_id": "53690",
  "source_file": "/.../FHM_transcript_combined/53690.txt",
  "model": "gpt-4o-mini",
  "schema_version": "1.0",
  "entry_info": {
    "indexer_initials": "...",
    "date_of_entry": "Apr 27, 2026",
    "piq_language": ["English"]
  },
  "interview": {
    "interview_date": "Nov 1, 2000",
    "interviewer_name": "Andrea Kowalski",
    ...
  },
  "interviewee": {
    "raw": { /* free-form Interviewee data exactly as the LLM produced it */ },
    "city_of_birth":  { "text": "Budapest", "keyword_id": 12345, "label": "Budapest (Hungary : city)", "is_proposed": false, "confidence": 0.97, "notes": "" },
    "country_of_birth": { ... },
    "religious_identity_prewar": { ... },
    "religious_identity_postwar": { ... },
    "ghettos": [ { "term": ResolvedTerm, "dates": "...", "notes": "..." }, ... ],
    "camps":   [ ... ],
    "prisons": [ ... ],
    "hiding_locations": [ { "location": ResolvedTerm, "types": [ResolvedTerm, ...], "notes": "..." }, ... ],
    "resistance_groups": [ ResolvedTerm, ... ],
    "who_liberated":    ResolvedTerm,
    "where_liberated":  ResolvedTerm,
    "other_attributes": [ ResolvedTerm, ... ],
    "special_events":   [ ResolvedTerm, ... ]
  },
  "family_people": [
    {
      "raw": { "first_name": "Yosef", "last_name": "Varga", ... },
      "place_of_birth": ResolvedTerm,
      "place_of_death": ResolvedTerm
    },
    ...
  ],
  "extraction_notes": "..."
}
```

`ResolvedTerm` always has the form:

```json
{
  "text": "free-form text from transcript",
  "keyword_id": 12345 | null,
  "label": "Auschwitz (Poland : Concentration Camp)(generic)" | null,
  "is_proposed": false,
  "confidence": 0.0 - 1.0,
  "notes": "judge's optional commentary"
}
```

If `is_proposed` is `true`, no good match was found in the choice group and
the indexer should review and propose a new keyword (per guideline 2.5.6).
For `special_events` (per guideline 2.5.17) proposals are disallowed;
unmatched entries are returned with `keyword_id: null` and `is_proposed:
false`.

---

## Project layout

```
.
├── FHM_transcript_combined/        # input transcripts (one per interview)
├── Jewish survivor question choices_22Apr2026.xlsx
├── INDEXING_GUIDELINES_REFERENCE.md
├── SAMPLE_INDEXING_DATA.md
├── indexing_agent/
│   ├── __init__.py
│   ├── schema.py                   # Pydantic models / output JSON schema
│   ├── choice_groups.py            # Excel loader + embedding cache
│   ├── extractor.py                # Stage 1: LLM extraction
│   ├── matcher.py                  # Stage 2: RAG term resolution
│   ├── pipeline.py                 # End-to-end per-transcript driver
│   └── cli.py                      # Command-line interface
├── output/                         # generated by the agent
├── .indexing_cache/                # generated embedding cache
├── requirements.txt
├── .env.example
└── README_INDEXING_AGENT.md        # this file
```

---

## Customising

- **Switch model**: pass `--extraction-model gpt-4o` (or any chat model
  that supports JSON-schema response format) for higher quality at higher
  cost.
- **Use a different vocabulary file**: `--xlsx /path/to/other.xlsx`.
- **Re-embed after vocabulary update**: delete `.indexing_cache/`. The
  cache key includes the workbook mtime, so changes are auto-detected.
- **Add new fields**: extend `indexing_agent/schema.py`, add a mapping in
  `choice_groups.FIELD_TO_QUESTION_SHEET` if the new field is backed by a
  choice group, and resolve it inside `matcher.resolve_indexing`.

---

## Known limitations

- The agent only works with English transcripts (the prompt is in English
  and assumes the `[INTERVIEWER]` / `[INTERVIEWEE]` tagging used by this
  project).
- Stage 2 makes one LLM judge call per indexing-term value. Transcripts
  with many family members and camps may take 30-90 s end-to-end.
- The judge sees only the top-K (default 15) most similar labels. If the
  correct label is buried deeper, raise `--top-k` (cost grows linearly).
- Indexer initials and date-of-entry are taken from whatever the LLM can
  glean from the transcript; in practice both are usually empty (they are
  set by the human indexer, not by the recording itself).
