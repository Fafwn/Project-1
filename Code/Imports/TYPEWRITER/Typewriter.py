import logging
from Imports.TYPEWRITER.STORYBOARD import STORYBOARD


logger = logging.getLogger(__name__)




book = STORYBOARD.Storyboard()

logger.info("Scene: %s" % book.get_scene(0))
logger.info("Scene: %s" % book.get_scene(9))



