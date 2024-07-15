"""imports = {
    "COMMANDS": ["MEMORY", "TRANSLATOR"],
    "SETTINGS": ["HANDLER", "VALUES"]
}


terminal = "" """

import logging
from STORYBOARD import STORYBOARD


logger = logging.getLogger(__name__)


def main():

    logging.basicConfig(format="%(levelname)s:%(filename)s:%(message)s", level=logging.INFO)
    logger.info('Gathering story TP 0')

    book = STORYBOARD.Storyboard()
    logger.info("Scene: %s" % book.run(0))
    logger.info('Gathering story TP 9')
    logger.info("Scene: %s" % book.run(9))

    logger.info('Finished')

if __name__ == '__main__':
    main()



