import logging

logger = logging.getLogger(__name__)


class Storyboard:
    MARKERS = {
        "SPA": "~",
        "END": "#",
        "JMP": "^",
        "RET": "/"
    }

    def __init__(self, story_file="STORYBOARD/STORYBOARD.txt"):
        self.TP = 0
        self.clean()
        self.story_file = story_file

        self.actions = {
            self.MARKERS["JMP"]: self.jump,
            self.MARKERS["RET"]: self.return_to
        }

    def run(self, start_position):
        self.clean()
        self.TP = start_position
        self.main()
        return self.scene

    def clean(self):
        self.scene = []
        self.RET_list = []

    def jump(self, command):
        self.RET_list.append(self.TP + 1)
        logging.debug("Return list:%s" % self.RET_list)
        self.TP = int(command)
        logging.debug("Jumping to %d" % self.TP)

    def return_to(self, command):
        self.TP = self.RET_list.pop()
        logging.debug("Returning to %d" % self.TP)

    def load_story(self):
        logging.info("Opening %s" % self.story_file)
        try:
            with open(self.story_file, "r") as story:
                raw = story.read().splitlines()
                logging.info("Story file opened.")
                return raw
        except FileNotFoundError:
            logging.error("%s not found." % self.story_file)
            return []

    def main(self):
        raw = self.load_story()
        if not raw:
            logging.error("Failed to load story, exiting...")
            return

        current = ""

        logging.info("Creating Stack")
        while current != self.MARKERS["END"]:
            current = raw[self.TP]
            if self.MARKERS["SPA"] in current:  # Normal message
                flags = current[:current.index(self.MARKERS["SPA"])]
                current = current[current.index(self.MARKERS["SPA"]) + 1:]
                logging.debug("TP:%d, Flags:%s @ %s" % (self.TP, flags, current))
                self.scene.append([current, flags])
                self.TP += 1
            else:  # Command
                flags = current[0]
                command = current[1:]
                logging.debug("Action: %s %s" % (flags, command))
                if flags in self.actions:
                    self.actions[flags](command)

        logging.info("Finished Stack")
        logging.debug("Scene: %s" % self.scene)
