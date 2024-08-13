import os
import logging
import sys
import importlib.util

logger = logging.getLogger(__name__)


def find_secondary():
    cwd = os.getcwd()
    code_dir = "Imports"
    seconds = (
        [part for part in [name for name in os.listdir(code_dir) if os.path.isdir(os.path.join(code_dir, name))] if
         os.path.isfile(f"{code_dir}/{part}/{part}.py")])
    seconds_dir = ["%s\%s\%s\%s.py" % (cwd, code_dir, part, part[0] + part[1:].lower()) for part in seconds]
    return seconds, seconds_dir


def import_secondary(modules):
    logger.debug("Importing Tier 2...")
    for name, directory in zip(modules[0], modules[1]):
        logger.debug("Importing second level - %s module [%s]" % (name, directory))
        spec = importlib.util.spec_from_file_location(name, directory)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        logger.debug("Imported %s" % name)
    logger.debug("Tier 2 done.")


def find_third():
    thirds = []
    thirds_dir = []
    return thirds, thirds_dir


def import_third(modules):
    logger.debug("Importing Tier 3...")

    logger.debug("Tier 3 done.")


def display():
    logger.debug([
        name for name, module in sys.modules.items() if
        hasattr(module, '__file__') and module.__file__ and module.__file__.startswith(
            os.path.dirname(os.path.abspath(__file__)))])
    logger.info("")


def run():
    logger.debug("Branch importer imported.")
    second = find_secondary()
    import_secondary(second)
    third = find_third()
    import_third(third)
    display()
