import os
import logging

logger = logging.getLogger(__name__)


class Storyboard:
    MARKERS = {
        "SPA": "~",
        "END": "#",
        "JMP": "^",
        "RET": "/"
    }

    def __init__(self, story_file="%s%s" % (os.getcwd(), "\Imports\TYPEWRITER\STORYBOARD\STORYBOARD.txt")):
        """
        Initialise Storyboard with default values

        :param story_file: Storyboard text file
        """

        self.TP = 0
        self.clean()
        self.story_file = story_file

        self.actions = {
            self.MARKERS["JMP"]: self.jump,
            self.MARKERS["RET"]: self.return_to
        }

    def get_scene(self, start_position):
        """
        Run the storyboard starting from given text pointer

        :param start_position: starting text pointer
        :return: [[str(message),str(flags)],...]
        """
        logger.info("Cleaning memory")
        self.clean()
        logger.info('Gathering story TP %d' % start_position)
        self.TP = start_position
        self.main()

        return self.scene

    def clean(self):
        """
        Cleans memory
        """
        self.scene = []
        self.RET_list = []

    def jump(self, command):
        """
        Handles Jump action
        :param command: which line to jump to
        """
        self.RET_list.append(self.TP + 1)
        logger.debug("Return list:%s" % self.RET_list)
        self.TP = int(command)
        logger.debug("Jumping to %d" % self.TP)

    def return_to(self, command):
        """
        Handles Return action
        :param command: Redundant
        """
        self.TP = self.RET_list.pop()
        logger.debug("Returning to %d" % self.TP)

    def load_story(self):
        """
        Loads story from story file
        """
        logger.info("Opening %s" % self.story_file)
        try:
            with open(self.story_file, "r") as story:
                raw = story.read().splitlines()
                logger.info("Story file opened.")
                return raw
        except FileNotFoundError:
            logger.error("%s not found." % self.story_file)
            return []

    def main(self):
        """
        Main function to process the story
        """
        raw = self.load_story()
        if not raw:
            logger.error("Failed to load story, exiting...")
            return

        current = ""

        logger.info("Creating Stack")
        while current != self.MARKERS["END"]:
            current = raw[self.TP]
            if self.MARKERS["SPA"] in current:  # Normal message
                flags = current[:current.index(self.MARKERS["SPA"])]
                current = current[current.index(self.MARKERS["SPA"]) + 1:]
                logger.debug("TP:%d, Flags:%s @ %s" % (self.TP, flags, current))
                self.scene.append([current, flags])
                self.TP += 1
            else:  # Command
                flags = current[0]
                command = current[1:]
                logger.debug("Action: %s %s" % (flags, command))
                if flags in self.actions:
                    self.actions[flags](command)

        logger.info("Finished Stack")
