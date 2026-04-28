"""End-to-end pipeline: transcript file -> validated `IndexingDocument`."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from openai import OpenAI

from .choice_groups import ChoiceGroup
from .extractor import extract_indexing
from .matcher import MatcherConfig, resolve_family_people, resolve_indexing
from .schema import IndexingDocument, RawIndexing

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    extraction_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    top_k: int = 15
    extraction_temperature: float = 0.0
    judge_temperature: float = 0.0


def _read_transcript(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def process_transcript(
    transcript_path: Path,
    output_dir: Path,
    client: OpenAI,
    choice_groups: Dict[str, ChoiceGroup],
    cfg: PipelineConfig,
    overwrite: bool = False,
) -> Optional[IndexingDocument]:
    transcript_id = transcript_path.stem
    out_path = output_dir / f"{transcript_id}.json"
    if out_path.exists() and not overwrite:
        logger.info("Skipping %s (already exists at %s)", transcript_id, out_path)
        return None

    transcript_text = _read_transcript(transcript_path)
    if not transcript_text:
        logger.warning("Empty transcript: %s", transcript_path)
        return None

    logger.info("[%s] Stage 1: extracting biographical fields", transcript_id)
    raw: RawIndexing = extract_indexing(
        client=client,
        model=cfg.extraction_model,
        transcript_id=transcript_id,
        transcript_text=transcript_text,
        temperature=cfg.extraction_temperature,
    )

    matcher_cfg = MatcherConfig(
        extraction_model=cfg.extraction_model,
        embedding_model=cfg.embedding_model,
        top_k=cfg.top_k,
        judge_temperature=cfg.judge_temperature,
    )

    logger.info("[%s] Stage 2a: resolving interviewee terms", transcript_id)
    interviewee_resolved = resolve_indexing(client, matcher_cfg, raw, choice_groups)

    logger.info(
        "[%s] Stage 2b: resolving family/people (%d entries)",
        transcript_id,
        len(raw.family_people),
    )
    family_resolved = resolve_family_people(client, matcher_cfg, raw, choice_groups)

    document = IndexingDocument(
        transcript_id=transcript_id,
        source_file=str(transcript_path),
        model=cfg.extraction_model,
        entry_info=raw.entry_info,
        interview=raw.interview,
        interviewee=interviewee_resolved,
        family_people=family_resolved,
        extraction_notes=raw.extraction_notes,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(document.model_dump_json(indent=2), encoding="utf-8")
    logger.info("[%s] Wrote %s", transcript_id, out_path)
    return document
