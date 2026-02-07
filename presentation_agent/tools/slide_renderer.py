import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

WIDTH = 1280
HEIGHT = 720

BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)

FONT_SIZE = 48


def render_slide(slide, output_path: Path):
    """
    slide can be:
    - dict: {"title": str, "content": list[str]}
    - list: [title, line1, line2, ...]  -> will be auto-converted
    """
    try:
        if isinstance(slide, list):
            logger.warning("Slide passed as list, converting to dict")
            slide = {"title": slide[0], "content": slide[1:]}

        title = slide.get("title", "")
        content_lines = slide.get("content", [])

        logger.info(f"Rendering slide: '{title}' -> {output_path}")

        img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("DejaVuSans.ttf", FONT_SIZE)
        except:
            font = ImageFont.load_default()

        full_text = title + "\n\n" + "\n".join(content_lines)
        wrapped_text = wrap_text(full_text, 40)

        draw.multiline_text(
            (100, 100),
            wrapped_text,
            fill=TEXT_COLOR,
            font=font,
            spacing=10
        )

        img.save(output_path)
        logger.info(f"Slide saved: {output_path}")

        return output_path

    except Exception:
        logger.exception("Slide render failed")
        raise


def render_all_slides(slides, output_dir: Path):
    try:
        logger.info("Rendering all slides")
        output_dir.mkdir(parents=True, exist_ok=True)

        paths = []
        for i, slide in enumerate(slides, start=1):
            filename = f"slide_{i:03d}.png"
            path = output_dir / filename
            render_slide(slide, path)
            paths.append(str(path))

        logger.info(f"{len(paths)} slides rendered")
        return paths

    except Exception:
        logger.exception("Render all slides failed")
        raise


def wrap_text(text, max_chars):
    lines = []
    words = text.split()
    line = ""

    for word in words:
        if len(line) + len(word) <= max_chars:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)
    return "\n".join(lines)
