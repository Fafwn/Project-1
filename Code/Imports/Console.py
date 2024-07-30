import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(filename)s:%(message)s", level=logging.INFO)


class Console:
    def __init__(self):
        self.terminal = ""  # acts as output
        self.content = ""  # acts as input

    def import_object(self, dir, object):
        logging.info("Importing object %s from %s" % (object, dir))
        pass

    def get(self, content):
        self.content = content

    def push(self, content=None):
        self.terminal = self.content if content == None else content
        self.flags["updated"] = True

    def peek(self):
        self.flags["updated"] = False
        return self.terminal
