import logging
from typing import Dict, Any, List
from dataclasses import make_dataclass, field, fields
from functools import lru_cache, cached_property
import os
from Code.Imports.ConfigMaster import Config
from Code.Imports import LogConfig

config = Config("WEAPON")
logger = logging.getLogger(__name__)

def create_weapon_info_class(details: List[Dict[str, Any]]):
    """
    Dynamically create a WeaponInfo class based on the detail's configuration.

    Args:
        details (List[Dict[str, Any]]): List of dictionaries defining the attributes.

    Returns:
        type: A dynamically created dataclass for WeaponInfo.
    """
    fields = []
    DEFAULTS = {
        "string": "",
        "integer": 0,
        "list": lambda: [],  # New list for each field
    }

    for detail in details:
        name = detail["name"]
        dtype = detail["type"]
        default = detail.get("default", None)

        # If the field name matches a key in the WEAPON config, use the first value from the config
        if name in config.data:
            default = config.data[name][0]  # Take the first value from the list in the YAML config

        # If default is still None, fall back to hardcoded DEFAULTS
        if default is None:
            default = DEFAULTS[dtype]() if callable(DEFAULTS[dtype]) else DEFAULTS[dtype]

        if dtype == "list":
            fields.append((name, List[str], field(default_factory=lambda d=default: d[:] if isinstance(d, list) else [])))
        elif dtype == "integer":
            fields.append((name, int, field(default=default)))
        elif dtype == "string":
            fields.append((name, str, field(default=default)))
        else:
            raise ValueError(f"Unsupported type '{dtype}' for field '{name}'.")

    # Dynamically create the WeaponInfo dataclass
    return make_dataclass("WeaponInfo", fields)


# Create the WeaponInfo class dynamically
WeaponInfo = create_weapon_info_class(config.data["details"])

class Weapon:
    PATH = os.path.dirname(os.path.abspath(__file__))
    EXTENSION = config.data["EXTENSION"]
    DIRECTORY = config.data["DIRECTORY"]
    SPACER = config.data["SPACER"]

    def __init__(self, reference: str):
        self.reference = reference
        self._info = None

    @cached_property
    def info(self) -> WeaponInfo:
        return self.parse_weapon_data()

    def __getitem__(self, key: str):
        return getattr(self.info, key)

    def get_weapon_path(self) -> str:
        return os.path.join(self.PATH, self.DIRECTORY, self.reference) + self.EXTENSION

    def read_reference(self) -> str:
        try:
            with open(self.get_weapon_path(), "r") as file:
                return file.read()
        except FileNotFoundError:
            logger.warning(f"Weapon file {self.get_weapon_path()} not found. Creating a default weapon.")
        except Exception as e:
            raise IOError(f"Error reading weapon file: {e}. Creating a default weapon.")
        return ""  # Return an empty string

    def write_weapon(self, info: WeaponInfo):
        data = self.SPACER.join(str(getattr(info, field.name)) for field in fields(info))
        try:
            with open(self.get_weapon_path(), "w") as file:
                file.write(data)
        except Exception as e:
            raise IOError(f"Error writing weapon data: {e}")

    @lru_cache(maxsize=None)
    def parse_weapon_data(self) -> WeaponInfo:
        raw_data = self.read_reference().split(self.SPACER) if self.read_reference() else []
        weapon_data = {}

        for i, field in enumerate(fields(WeaponInfo)):
            try:
                raw_value = raw_data[i] if i < len(raw_data) else ""

                if field.type == List[str]:
                    weapon_data[field.name] = raw_value.split(",") if raw_value else []
                elif raw_value == "":
                    weapon_data[field.name] = getattr(WeaponInfo, field.name)
                    default_value = getattr(WeaponInfo, field.name)
                    logger.warning(f"Missing data for field '{field.name}' in weapon '{self.reference}'."
                                   f" Using default value: {default_value}")
                else:
                    parsed_value = field.type(raw_value) if raw_value else field.type()

                    if field.name in config.data and isinstance(config.data[field.name], list):
                        allowed_values = config.data[field.name]
                        if parsed_value not in allowed_values:
                            default_value = allowed_values[0]
                            logger.warning(
                                f"Invalid value '{parsed_value}' for field '{field.name}' in weapon '{self.reference}'."
                                f"Allowed values are {allowed_values}. Using default value: {default_value}"
                            )
                            parsed_value = default_value

                    weapon_data[field.name] = parsed_value

            except (ValueError, TypeError):
                default_value = getattr(WeaponInfo, field.name)
                weapon_data[field.name] = default_value
                logger.warning(
                    f"Missing or invalid data for field '{field.name}' in weapon '{self.reference}'."
                    f"Using default value: {default_value}"
                )

        return WeaponInfo(**weapon_data)


# Example Usage
if __name__ == "__main__":
    weapon = Weapon("OMGEE")
    print(weapon.info)