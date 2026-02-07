import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

WIDTH = 1280
HEIGHT = 720

BACKGROUND_COLOR = (30, 30, 30)
TITLE_COLOR = (255, 255, 255)
BODY_COLOR = (200, 200, 200)

TITLE_FONT_SIZE = 60
BODY_FONT_SIZE = 40


def render_slide(slide: dict, output_path: Path):
    """
    Renders a single slide to PNG image.

    slide format:
    {
        "title": "...",
        "content": ["line1", "line2", ...]
    }
    """

    try:
        logger.info(f"Rendering slide: {output_path}")

        title = slide["title"]
        content_lines = slide["content"]

        img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        # Load fonts
        try:
            title_font = ImageFont.truetype("DejaVuSans.ttf", TITLE_FONT_SIZE)
            body_font = ImageFont.truetype("DejaVuSans.ttf", BODY_FONT_SIZE)
        except Exception:
            logger.warning("Custom font not found, using default font")
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()

        # Draw title
        y = 80
        draw.text((100, y), title, font=title_font, fill=TITLE_COLOR)

        # Draw content
        y += 120

        for line in content_lines:

            wrapped = wrap_text(line, 50)

            for wrapped_line in wrapped.split("\n"):
                draw.text((100, y), wrapped_line, font=body_font, fill=BODY_COLOR)
                y += 60

            y += 20  # spacing between paragraphs

        # Save image
        output_path.parent.mkdir(parents=True, exist_ok=True)

        img.save(output_path)

        logger.info(f"Slide saved successfully: {output_path}")

        return output_path

    except Exception:
        logger.exception("Slide render failed")
        raise


def render_all_slides(slides: list, output_dir: Path):
    """
    Renders all slides and returns list of image paths.
    """

    try:
        logger.info("Rendering all slides")

        output_dir.mkdir(parents=True, exist_ok=True)

        paths = []

        for i, slide in enumerate(slides, start=1):

            filename = f"slide_{i:03d}.png"

            path = output_dir / filename

            render_slide(slide, path)

            paths.append(str(path))

        logger.info(f"{len(paths)} slides rendered successfully")

        return paths

    except Exception:
        logger.exception("Render all slides failed")
        raise


def wrap_text(text: str, max_chars: int):

    words = text.split()

    lines = []

    current = ""

    for word in words:

        if len(current) + len(word) + 1 <= max_chars:
            current += word + " "
        else:
            lines.append(current.strip())
            current = word + " "

    if current:
        lines.append(current.strip())

    return "\n".join(lines)
