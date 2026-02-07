import logging
from fastapi import FastAPI, HTTPException
from pathlib import Path

from presentation_agent.tools.parser import parse_file

logger = logging.getLogger(__name__)

INPUT_DIR = Path("presentation_agent/workspace/input")
OUTPUT_DIR = Path("presentation_agent/workspace/output")

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/parse")
def parse_endpoint(fileName: str):
    try:

        file_path = INPUT_DIR / fileName

        slides = parse_file(file_path)

        return {
            "file": fileName,
            "slides": slides,
            "count": len(slides)
        }

    except Exception as e:
        logger.exception("Parse endpoint failed")
        raise HTTPException(status_code=500, detail=str(e))
