from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import logging

from presentation_agent.agents.input_agent import InputAgent
from presentation_agent.tools.slide_renderer import render_slide
from presentation_agent.tools.video_renderer import create_video

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

# Directories
INPUT_DIR = Path("/app/workspace/input")
OUTPUT_DIR = Path("/app/workspace/output")
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# FastAPI app
app = FastAPI(title="Presentation Video Generator")


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


@app.post("/render")
def render_endpoint(fileName: str):

    try:

        file_path = INPUT_DIR / fileName

        slides = parse_file(file_path)

        image_paths = render_all_slides(slides, OUTPUT_DIR)

        return {
            "images": image_paths,
            "count": len(image_paths)
        }

    except Exception as e:

        logger.exception("Render endpoint failed")

        raise HTTPException(status_code=500, detail=str(e))



@app.post("/generate")
async def generate(file: UploadFile = File(...)):
    """
    Upload a text file, generate a video, and return the output file path.
    """
    try:
        input_file_path = INPUT_DIR / file.filename
        with open(input_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        logger.info(f"Video generation started for {input_file_path}")

        # Step 2: Parse slides
        slides = InputAgent().run(input_file_path)
        logger.info(f"Slides processed: {len(slides)}")

        # Step 3: Render slides to images
        images = render_slide(slides)
        logger.info(f"Generated {len(images)} slide images")

        # Step 4: Create video
        output_file_path = OUTPUT_DIR / f"{input_file_path.stem}.mp4"
        create_video(images, output_file_path)

        logger.info(f"Video generation completed: {output_file_path}")
        return {"video_path": str(output_file_path)}

    except Exception as e:
        logger.error(f"Video generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{video_name}")
def download_video(video_name: str):
    """
    Download the video by file name.
    """
    video_path = OUTPUT_DIR / video_name
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video_path, media_type="video/mp4", filename=video_name)
