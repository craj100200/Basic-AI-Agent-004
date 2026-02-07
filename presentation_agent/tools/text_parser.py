import logging
import re

logger = logging.getLogger(__name__)


class TextParser:
    """
    Parses presentation text into structured slides.
    """

    def parse(self, text: str):

        try:
            logger.info("Parsing started")

            slides = []

            slide_blocks = re.findall(
                r'\[SLIDE_START\](.*?)\[SLIDE_END\]',
                text,
                re.DOTALL
            )

            for block in slide_blocks:

                title_match = re.search(
                    r'\[TITLE_START\](.*?)\[TITLE_END\]',
                    block,
                    re.DOTALL
                )

                title = title_match.group(1).strip() if title_match else ""

                content = re.sub(
                    r'\[TITLE_START\].*?\[TITLE_END\]',
                    '',
                    block,
                    flags=re.DOTALL
                ).strip()

                slides.append({
                    "title": title,
                    "content": content
                })

            logger.info(f"{len(slides)} slides parsed")

            return slides

        except Exception as e:
            logger.exception("Parsing failed")
            raise e
