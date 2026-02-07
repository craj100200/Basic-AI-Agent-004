import logging
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File

from presentation_agent.agents.input_agent import InputAgent


# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


# FastAPI app
app = FastAPI()


# Paths
ROOT_DIR = Path(__file__).resolve().parent

WORKSPACE_DIR = ROOT_DIR / "workspace"
INPUT_DIR = WORKSPACE_DIR / "input"
OUTPUT_DIR = WORKSPACE_DIR / "output"


# Ensure folders exist
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/parse-file")
async def parse_file(file: UploadFile = File(...)):

    try:

        file_path = INPUT_DIR / file.filename

        logger.info(f"Saving file to {file_path}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        slides = InputAgent().run(str(file_path))

        return {
            "status": "success",
            "slide_count": len(slides),
            "slides": slides
        }

    except Exception as e:

        logger.exception("parse-file failed")

        return {
            "status": "error",
            "message": str(e)
        }
