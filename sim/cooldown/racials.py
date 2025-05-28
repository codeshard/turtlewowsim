from sim.character import Character

from .base import Cooldown


class Berserking(Cooldown):
    @property
    def duration(self):
        return 10

    @property
    def cooldown(self):
        return 180

    def __init__(self, character: Character, haste: float):
        super().__init__(character)
        self.haste = haste

    def activate(self):
        super().activate()
        self.character.add_trinket_haste(self.name, self.haste)

    def deactivate(self):
        super().deactivate()
        self.character.remove_trinket_haste(self.name)


class BloodFury(Cooldown):
    @property
    def duration(self):
        return 15

    @property
    def cooldown(self):
        return 120

    def activate(self):
        super().activate()
        self.character.add_sp_bonus(60)

    def deactivate(self):
        super().deactivate()
        self.character.remove_sp_bonus(60)


class Perception(Cooldown):
    @property
    def duration(self):
        return 20

    @property
    def cooldown(self):
        return 180

    def activate(self):
        super().activate()
        self.character.add_crit_bonus(2)

    def deactivate(self):
        super().deactivate()
        self.character.remove_crit_bonus(2)
