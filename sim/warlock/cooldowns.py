from sim.cooldown import Cooldown


class ConflagrateCooldown(Cooldown):
    @property
    def duration(self):
        return 0

    @property
    def cooldown(self):
        return 10


class SoulFireCooldown(Cooldown):
    @property
    def duration(self):
        return 0

    @property
    def cooldown(self):
        return 30


class DarkHarvestCooldown(Cooldown):
    @property
    def duration(self):
        return 0

    @property
    def cooldown(self):
        return 30
