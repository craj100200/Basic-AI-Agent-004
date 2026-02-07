import logging
from presentation_agent.tools.text_parser import TextParser

logger = logging.getLogger(__name__)


class InputAgent:

    def __init__(self):
        self.parser = TextParser()

    def run(self, file_path: str):

        try:
            logger.info(f"Reading file {file_path}")

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            slides = self.parser.parse(text)

            logger.info("InputAgent completed")

            return slides

        except Exception as e:
            logger.exception("InputAgent failed")
            raise e
