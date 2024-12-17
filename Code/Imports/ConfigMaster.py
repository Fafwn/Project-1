import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import inspect

logger = logging.getLogger(__name__)

class Config:
    """
    A class to manage configuration settings for different modules.
    """
    _cached_config: Optional[Dict[str, Any]] = None
    _config_path: Optional[Path] = None

    def __init__(self, module_name: str):
        """
        Initialize the Config object for a specific module.

        Args:
            module_name (str): The name of the module to load configuration for.
        """
        self.module_name = module_name
        self.data = self.get_config()

    @classmethod
    def resolve_config_path(cls) -> Path:
        """
        Resolve the path to the configuration file dynamically based on the importing file's directory.

        Returns:
            Path: The resolved path to the configuration file.
        """
        if cls._config_path is not None:
            return cls._config_path

        # Inspect the call stack to find the importing file
        stack = inspect.stack()
        for frame_info in stack:
            if frame_info.filename != __file__:  # Ignore ConfigMaster itself
                importing_file = frame_info.filename
                importing_dir = Path(importing_file).parent
                break
        else:
            logger.error("Could not determine the importing file.")
            raise RuntimeError("Unable to resolve the configuration path.")

        # Look for a config.yaml in the importing file's directory
        config_path = importing_dir / "config.yaml"
        if not config_path.exists():
            logger.error(f"Configuration file {config_path} not found.")
            raise FileNotFoundError(f"No configuration file found in {importing_dir}.")

        logger.info(f"Resolved configuration file path: {config_path}")
        cls._config_path = config_path
        return cls._config_path

    @classmethod
    def load_config_file(cls) -> Dict[str, Any]:
        """
        Load the configuration file and cache it.

        Returns:
            Dict[str, Any]: The loaded configuration data.
        """
        if cls._cached_config is not None:
            return cls._cached_config

        config_path = cls.resolve_config_path()

        try:
            with config_path.open("r") as file:
                cls._cached_config = yaml.safe_load(file) or {}
            logger.info(f"Successfully loaded configuration from {config_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration file {config_path}: {e}")
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
        cls._config_path = None
        cls.load_config_file()
        logger.info("Configuration reloaded")
