import WeaponHandler

class Character:
    def __init__(self):
        self.info = {
            "Name": "",
            "Weapon": None
        }
        self.stats = {
            "Level": 1,
            "Strength": 3,
            "Wisdom": 1,
            "Dexterity": 2,
            "Defence": 0,
            "Resistance":2,
            "Luck": 0,
            "Critical": 5
        }
        self.hidden_stats = {
            "Attack": 0,
            "Hit": 0,
            "Avoid": 0,
            "Critical": 0
        }


    def calculate_stats(self):
        calc_stats = {
            "Attack": 0,
            "Hit": 0,
            "Avoid": 0,
            "Critical": 0
        }

        return calc_stats

    def select_weapon(self, weapon):
        self.info["Weapon"] = WeaponHandler.Weapon(weapon)
        print(self.info["Weapon"].info)


if __name__ == "__main__":
    char = Character()
    char.select_weapon("weapon1")


