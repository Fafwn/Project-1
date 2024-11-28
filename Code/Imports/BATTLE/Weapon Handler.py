from typing import Dict, Any, List
from dataclasses import dataclass, field
from functools import lru_cache, cached_property


@dataclass
class WeaponInfo:
    """
    A dataclass representing information about a weapon.

    Attributes:
        Name (str): The name of the weapon.
        Might (int): The power or strength of the weapon.
        Range (int): The effective range of the weapon.
        Hit (int): The accuracy of the weapon.
        Critical (int): The critical hit rate of the weapon.
        Weight (int): The weight of the weapon.
        Description (str): A brief description of the weapon.
        Sprites (List[str]): A list of sprite filenames for the weapon.
        Current_Sprite (int): The index of the currently active sprite.
        Animations (List[str]): A list of animation filenames for the weapon.
        Current_Animation (int): The index of the currently active animation.
    """

    Name: str = ""
    Might: int = 0
    Range: int = 1
    Hit: int = 0
    Critical: int = 0
    Weight: int = 1
    Description: str = ""
    Sprites: List[str] = field(default_factory=list)
    Current_Sprite: int = 0
    Animations: List[str] = field(default_factory=list)
    Current_Animation: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create a WeaponInfo instance from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing weapon information.

        Returns:
            WeaponInfo: A new WeaponInfo instance with attributes set from the input dictionary.
        """
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    @classmethod
    def to_dict(cls, instance) -> Dict[str, Any]:
        """
        Convert a WeaponInfo instance to a dictionary.

        Args:
            instance (WeaponInfo): The WeaponInfo instance to convert.

        Returns:
            Dict[str, Any]: A dictionary representation of the WeaponInfo instance.
        """
        return {k: getattr(instance, k) for k in cls.__annotations__}

class Weapon:
    PATH = "C:/Users/kaiki/IdeaProjects/Project-1/Code/Imports/BATTLE/Weapons/"
    EXTENSION = ".kj"
    SPACER = ";"

    def __init__(self, reference: str):
        """
        Initialize a Weapon instance.

        Args:
            reference (str): The reference name of the weapon file.
        """
        self.reference = reference
        self._info = None

    @cached_property
    def info(self) -> WeaponInfo:
        """
        Get the WeaponInfo for this weapon.

        Returns:
            WeaponInfo: The parsed weapon information.
        """
        return self.parse_weapon_data()

    def __getitem__(self, key: str):
        """
        Get an attribute of the weapon's info.

        Args:
            key (str): The name of the attribute to retrieve.

        Returns:
            Any: The value of the requested attribute.
        """
        return getattr(self.info, key)

    def get_weapon_path(self) -> str:
        """
        Get the full file path for the weapon.

        Returns:
            str: The complete file path for the weapon.
        """
        return f"{self.PATH}{self.reference}{self.EXTENSION}"

    def read_reference(self) -> str:
        """
        Read the contents of the weapon file.

        Returns:
            str: The contents of the weapon file.

        Raises:
            FileNotFoundError: If the weapon file is not found.
            IOError: If there's an error reading the weapon file.
        """
        try:
            with open(self.get_weapon_path(), "r") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Weapon file {self.get_weapon_path()} not found.")
        except Exception as e:
            raise IOError(f"Error reading weapon file: {e}")

    def write_weapon(self, info: WeaponInfo):
        """
        Write the weapon information to the weapon file.

        Args:
            info (WeaponInfo): The weapon information to write.

        Raises:
            IOError: If there's an error writing the weapon data.
        """
        data = self.SPACER.join(",".join(value) if isinstance(value, list) else str(value)
                                for value in WeaponInfo.to_dict(info).values())
        try:
            with open(self.get_weapon_path(), "w") as file:
                file.write(data)
        except Exception as e:
            raise IOError(f"Error writing weapon data: {e}")

    @lru_cache(maxsize=None)
    def parse_weapon_data(self) -> WeaponInfo:
        """
        Parse the weapon data from the weapon file.

        Returns:
            WeaponInfo: A WeaponInfo object containing the parsed weapon data.
        """
        raw_data = self.read_reference().split(self.SPACER)
        weapon_data = {}
        for (name, field_type), raw_value in zip(WeaponInfo.__annotations__.items(), raw_data):
            try:
                if field_type == List[str]:
                    weapon_data[name] = raw_value.split(",") if raw_value else []
                else:
                    weapon_data[name] = field_type(raw_value)
            except (ValueError, TypeError, IndexError):
                weapon_data[name] = getattr(WeaponInfo, name)
        return WeaponInfo.from_dict(weapon_data)

# Example Usage
if __name__ == "__main__":
    weapon = Weapon("Weapon1")
    print(weapon.info)  # Should print a detailed WeaponInfo object