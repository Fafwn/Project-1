import logging

import STORYBOARD


"""imports = {
    "COMMANDS": ["MEMORY", "TRANSLATOR"],
    "SETTINGS": ["HANDLER", "VALUES"],
    "STORYBOARD": ["STORYBOARD"]
}"""

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(filename)s:%(message)s", level=logging.INFO)

def run():

    book = STORYBOARD.Storyboard()

    logger.info("Scene: %s" % book.get_scene(0))
    logger.info("Scene: %s" % book.get_scene(9))



