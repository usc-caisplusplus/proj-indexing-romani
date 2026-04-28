"""Command-line entry point.

Examples:

    # Index a single transcript
    python -m indexing_agent.cli --ids 53690

    # Index a few transcripts
    python -m indexing_agent.cli --ids 53690,53691,53692

    # Index everything (resumable: skips files already in output/)
    python -m indexing_agent.cli --all

    # Force re-index
    python -m indexing_agent.cli --ids 53690 --overwrite

    # Just rebuild the embedding cache and exit
    python -m indexing_agent.cli --build-cache-only
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

from .choice_groups import load_all_choice_groups
from .pipeline import PipelineConfig, process_transcript


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)


def _resolve_ids(
    project_root: Path,
    transcript_dir: Path,
    ids: Optional[List[str]],
    process_all: bool,
    limit: Optional[int],
) -> List[Path]:
    if ids:
        paths = []
        for id_ in ids:
            path = transcript_dir / f"{id_}.txt"
            if not path.exists():
                raise FileNotFoundError(path)
            paths.append(path)
        return paths

    if process_all:
        paths = sorted(transcript_dir.glob("*.txt"))
        if limit:
            paths = paths[:limit]
        return paths

    return []


def main(argv: Optional[List[str]] = None) -> int:
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(project_root / ".env", override=False)

    parser = argparse.ArgumentParser(description="USC Shoah Foundation indexing agent")
    parser.add_argument(
        "--transcript-dir",
        type=Path,
        default=project_root / "FHM_transcript_combined",
        help="Directory containing combined transcript .txt files.",
    )
    parser.add_argument(
        "--xlsx",
        type=Path,
        default=project_root / "Jewish survivor question choices_22Apr2026.xlsx",
        help="Path to the Excel choice-group workbook.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=project_root / "output",
        help="Where to write per-transcript JSON files.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=project_root / ".indexing_cache",
        help="Where to cache choice-group embeddings.",
    )
    parser.add_argument("--ids", type=str, default=None, help="Comma-separated transcript IDs (e.g. 53690,53691).")
    parser.add_argument("--all", action="store_true", help="Process every transcript in --transcript-dir.")
    parser.add_argument("--limit", type=int, default=None, help="Cap the number of transcripts (with --all).")
    parser.add_argument("--overwrite", action="store_true", help="Re-process even if output JSON already exists.")
    parser.add_argument("--top-k", type=int, default=15, help="Top-K candidates retrieved per term.")
    parser.add_argument(
        "--extraction-model",
        default=os.getenv("OPENAI_EXTRACTION_MODEL", "gpt-4o-mini"),
        help="OpenAI chat model used for extraction + judging.",
    )
    parser.add_argument(
        "--embedding-model",
        default=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        help="OpenAI embedding model used for choice-group retrieval.",
    )
    parser.add_argument("--build-cache-only", action="store_true", help="Build embedding cache and exit.")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    _setup_logging(args.verbose)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "ERROR: OPENAI_API_KEY is not set. Copy .env.example to .env and "
            "fill in your key, or `export OPENAI_API_KEY=...`.",
            file=sys.stderr,
        )
        return 2

    client = OpenAI(api_key=api_key)

    logging.info("Loading / building choice-group embeddings (cache: %s)", args.cache_dir)
    choice_groups = load_all_choice_groups(
        xlsx_path=args.xlsx,
        cache_dir=args.cache_dir,
        client=client,
        embed_model=args.embedding_model,
    )
    logging.info("Loaded %d choice groups", len(choice_groups))

    if args.build_cache_only:
        return 0

    ids = args.ids.split(",") if args.ids else None
    transcripts = _resolve_ids(
        project_root=project_root,
        transcript_dir=args.transcript_dir,
        ids=ids,
        process_all=args.all,
        limit=args.limit,
    )

    if not transcripts:
        print("Nothing to do. Pass --ids X,Y,Z or --all.", file=sys.stderr)
        return 1

    cfg = PipelineConfig(
        extraction_model=args.extraction_model,
        embedding_model=args.embedding_model,
        top_k=args.top_k,
    )

    failed: List[str] = []
    for path in tqdm(transcripts, desc="transcripts", unit="file"):
        try:
            process_transcript(
                transcript_path=path,
                output_dir=args.output_dir,
                client=client,
                choice_groups=choice_groups,
                cfg=cfg,
                overwrite=args.overwrite,
            )
        except Exception as exc:  # pragma: no cover - top-level safety net
            logging.exception("Failed to process %s: %s", path.name, exc)
            failed.append(path.name)

    if failed:
        print(f"\nCompleted with {len(failed)} failures: {failed}", file=sys.stderr)
        return 1
    print(f"\nDone. Output in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
