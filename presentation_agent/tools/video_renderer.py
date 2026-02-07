import logging
from pathlib import Path
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

OUTPUT_DIR = Path("/app/workspace/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_video(image_files: list, output_file: Path = None, fps: int = 1):
    """
    Generate a video from a list of image files.
    :param image_files: List of Paths to slide images
    :param output_file: Path to output video file (MP4)
    :param fps: Frames per second
    :return: Path to generated video
    """
    if not image_files:
        raise ValueError("No image files provided for video generation.")
    
    if output_file is None:
        output_file = OUTPUT_DIR / "presentation_video.mp4"

    try:
        # Convert Path objects to strings
        image_paths = [str(f) for f in image_files]

        logger.info(f"Creating video from {len(image_paths)} images at {fps} fps.")
        clip = ImageSequenceClip(image_paths, fps=fps)
        clip.write_videofile(str(output_file), codec="libx264", audio=False)
        logger.info(f"Video saved: {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Failed to create video: {e}")
        raise
