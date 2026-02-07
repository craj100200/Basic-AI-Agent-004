import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def parse_file(file_path: Path):
    try:
        logger.info(f"Parsing file: {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} not found")

        text = file_path.read_text(encoding="utf-8")

        slides = [
            slide.strip()
            for slide in text.split("\n\n")
            if slide.strip()
        ]

        logger.info(f"Parsed {len(slides)} slides")

        return slides

    except Exception as e:
        logger.exception("Parser failed")
        raise
