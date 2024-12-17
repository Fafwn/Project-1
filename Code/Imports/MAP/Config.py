import yaml
import logging

"""
config_path = "C:/Users/kaiki/IdeaProjects/Project-1/Code/Imports/MAP/config.yaml"
logger = logging.getLogger(__name__)


class Config:
    def __init__(self, module_name):
        self.module_name = module_name
        self.data = self.get_config()

    def get_config(self):
        with open(config_path, "r") as file:
            config_data = yaml.safe_load(file)
        if self.module_name in config_data:
            return config_data.get(self.module_name, {})
        else:
            logger.critical(f"Module {self.module_name} not found in config.yaml")
"""