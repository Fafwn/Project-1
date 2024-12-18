import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path

CONFIG_PATH = Path("C:/Users/kaiki/IdeaProjects/Project-1/Code/Imports/BATTLE/config.yaml")
logger = logging.getLogger(__name__)

class Config:
    """
    A class to manage configuration settings for different modules.
    """

    _cached_config: Optional[Dict[str, Any]] = None

    def __init__(self, module_name: str):
        """
        Initialize the Config object for a specific module.

        Args:
            module_name (str): The name of the module to load configuration for.
        """
        self.module_name = module_name
        self.data = self.get_config()

    @classmethod
    def load_config_file(cls) -> Dict[str, Any]:
        """
        Load the configuration file and cache it.

        Returns:
            Dict[str, Any]: The loaded configuration data.
        """
        if cls._cached_config is not None:
            return cls._cached_config

        try:
            with CONFIG_PATH.open("r") as file:
                cls._cached_config = yaml.safe_load(file)
            logger.info(f"Successfully loaded configuration from {CONFIG_PATH}")
        except FileNotFoundError:
            logger.error(f"Configuration file {CONFIG_PATH} not found")
            cls._cached_config = {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration file {CONFIG_PATH}: {e}")
            cls._cached_config = {}
        except Exception as e:
            logger.error(f"Unexpected error loading configuration file: {e}")
            cls._cached_config = {}

        return cls._cached_config

    def get_config(self) -> Dict[str, Any]:
        """
        Get the configuration for the specific module.

        Returns:
            Dict[str, Any]: The configuration data for the module.
        """
        config_data = self.load_config_file()
        if self.module_name in config_data:
            return config_data[self.module_name]
        else:
            logger.warning(f"Module '{self.module_name}' not found in config.yaml")
            return {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a specific configuration value for the module.

        Args:
            key (str): The configuration key to retrieve.
            default (Any, optional): The default value to return if the key is not found.

        Returns:
            Any: The configuration value for the given key, or the default value if not found.
        """
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """
        Allow dictionary-style access to configuration values.

        Args:
            key (str): The configuration key to retrieve.

        Returns:
            Any: The configuration value for the given key.

        Raises:
            KeyError: If the key is not found in the configuration.
        """
        if key in self.data:
            return self.data[key]
        raise KeyError(f"Configuration key '{key}' not found for module '{self.module_name}'")

    @classmethod
    def reload_config(cls) -> None:
        """
        Force a reload of the configuration file, clearing the cache.
        """
        cls._cached_config = None
        cls.load_config_file()
        logger.info("Configuration reloaded")