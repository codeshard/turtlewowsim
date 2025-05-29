from typing import TYPE_CHECKING

from sim.spell_school import DamageType
from .base import Cooldown

if TYPE_CHECKING:
    from sim.character import Character

class MindQuickeningGem(Cooldown):
    # Mind Quickening Gem
    @property
    def duration(self):
        return 20

    @property
    def cooldown(self):
        return 300

    def activate(self):
        super().activate()
        self.character.add_trinket_haste(self.name, 33)

    def deactivate(self):
        super().deactivate()
        self.character.remove_trinket_haste(self.name)


class TalismanofEphemeralPower(Cooldown):
    # Talisman of Ephemeral Power
    DMG_BONUS = 175

    @property
    def duration(self):
        return 15

    @property
    def cooldown(self):
        return 90

    def activate(self):
        super().activate()
        self.character.add_sp_bonus(self.DMG_BONUS)

    def deactivate(self):
        super().deactivate()
        self.character.remove_sp_bonus(self.DMG_BONUS)


class ZandalarianHeroCharm(Cooldown):
    def __init__(self, character: "Character"):
        super().__init__(character)
        self._initial_sp_bonus = 204
        self._current_sp_bonus = 0

    @property
    def cooldown(self):
        return 120

    @property
    def duration(self):
        return 20

    def use_charge(self):
        if self._current_sp_bonus > 0:
            deduction = min(17, self._current_sp_bonus)
            self._current_sp_bonus -= deduction

            # deduct from character
            self.character.remove_sp_bonus(deduction)

    def activate(self):
        super().activate()
        self._current_sp_bonus = self._initial_sp_bonus
        self.character.add_sp_bonus(self._current_sp_bonus)

    def deactivate(self):
        super().deactivate()
        self.character.remove_sp_bonus(self._current_sp_bonus)
        self._current_sp_bonus = 0


class RestrainedEssenceofSapphiron(Cooldown):
    # Restrained Essence of Sapphiron
    DMG_BONUS = 130

    @property
    def duration(self):
        return 20

    @property
    def cooldown(self):
        return 120

    def activate(self):
        super().activate()
        self.character.add_sp_bonus(self.DMG_BONUS)

    def deactivate(self):
        super().deactivate()
        self.character.remove_sp_bonus(self.DMG_BONUS)


class PotionOfQuickness(Cooldown):
    @property
    def cooldown(self):
        return 120

    @property
    def duration(self):
        return 30

    def activate(self):
        super().activate()
        self.character.add_consume_haste(self.name, 5)

    def deactivate(self):
        super().deactivate()
        self.character.remove_consume_haste(self.name)


class WrathOfCenariusBuff(Cooldown):
    DMG_BONUS = 132
    PRINTS_ACTIVATION = True
    TRACK_UPTIME = True

    def __init__(self, character: "Character"):
        super().__init__(character)
        self._buff_end_time = -1

    @property
    def usable(self):
        return not self._active

    @property
    def duration(self):
        return 10

    # need special handling for when cooldown ends due to possibility of cooldown reset # noqa E501
    def activate(self):
        if self.usable:
            self.character.add_sp_bonus(self.DMG_BONUS)

            if self.TRACK_UPTIME:
                self.track_buff_start_time()

            self._buff_end_time = self.character.env.now + self.duration

            self._active = True
            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} activated")

            def callback(self):
                while True:
                    remaining_time = (
                        self._buff_end_time - self.character.env.now
                    )
                    yield self.character.env.timeout(remaining_time)

                    if self.character.env.now >= self._buff_end_time:
                        self.deactivate()
                        break

            self.character.env.process(callback(self))
        else:
            # refresh buff end time
            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} refreshed")
            self._buff_end_time = self.character.env.now + self.duration

    def deactivate(self):
        super().deactivate()
        self.character.remove_sp_bonus(self.DMG_BONUS)


class EndlessGulchBuff(Cooldown):
    PRINTS_ACTIVATION = True
    TRACK_UPTIME = True

    def __init__(self, character: "Character"):
        super().__init__(character)
        self._buff_end_time = -1

    @property
    def duration(self):
        return 15

    # need special handling for when cooldown ends due to possibility of refresh # noqa E501
    def activate(self):
        if self.usable:
            self.character.add_trinket_haste(self.name, 20)

            if self.TRACK_UPTIME:
                self.track_buff_start_time()

            self._buff_end_time = self.character.env.now + self.duration

            self._active = True
            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} activated")

            def callback(self):
                while True:
                    remaining_time = (
                        self._buff_end_time - self.character.env.now
                    )
                    yield self.character.env.timeout(remaining_time)

                    if self.character.env.now >= self._buff_end_time:
                        self.deactivate()
                        break

            self.character.env.process(callback(self))
        else:
            # refresh buff end time
            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} refreshed")
            self._buff_end_time = self.character.env.now + self.duration

    def deactivate(self):
        super().deactivate()
        self.character.remove_trinket_haste(self.name)


class CharmOfMagic(Cooldown):
    """
    Use: Increases the critical hit chance of your Arcane spells by 5%, and
    increases the critical hit damage of your Arcane spells by 50% for 20 sec.
    """

    @property
    def cooldown(self):
        return 180

    @property
    def duration(self):
        return 20

    def activate(self):
        super().activate()
        self.character.damage_type_crit[DamageType.ARCANE] += 5
        self.character.damage_type_crit_mult[DamageType.ARCANE] += 0.25

    def deactivate(self):
        super().deactivate()
        self.character.damage_type_crit[DamageType.ARCANE] -= 5
        self.character.damage_type_crit_mult[DamageType.ARCANE] -= 0.25


class TrueBandOfSulfurasBuff(Cooldown):
    PRINTS_ACTIVATION = True
    TRACK_UPTIME = True

    def __init__(self, character: "Character"):
        super().__init__(character)
        self._buff_end_time = -1

    @property
    def duration(self):
        return 6

    # need special handling for when cooldown ends due to possibility of refresh # noqa E501
    def activate(self):
        if self.usable:
            self.character.add_trinket_haste(self.name, 5)

            if self.TRACK_UPTIME:
                self.track_buff_start_time()

            self._buff_end_time = self.character.env.now + self.duration

            self._active = True
            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} activated")

            def callback(self):
                while True:
                    remaining_time = (
                        self._buff_end_time - self.character.env.now
                    )
                    yield self.character.env.timeout(remaining_time)

                    if self.character.env.now >= self._buff_end_time:
                        self.deactivate()
                        break

            self.character.env.process(callback(self))
        else:
            # refresh buff end time
            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} refreshed")
            self._buff_end_time = self.character.env.now + self.duration

    def deactivate(self):
        super().deactivate()
        self.character.remove_trinket_haste(self.name)


class BindingsOfContainedMagicBuff(Cooldown):
    DMG_BONUS = 100
    PRINTS_ACTIVATION = True
    TRACK_UPTIME = True

    def __init__(self, character: "Character"):
        super().__init__(character)
        self._buff_end_time = -1

    @property
    def usable(self):
        return not self._active

    @property
    def duration(self):
        return 6

    def activate(self):
        if self.usable:
            self.character.add_sp_bonus(self.DMG_BONUS)

            if self.TRACK_UPTIME:
                self.track_buff_start_time()

            self._buff_end_time = self.character.env.now + self.duration

            self._active = True
            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} activated")

            def callback(self):
                while True:
                    remaining_time = (
                        self._buff_end_time - self.character.env.now
                    )
                    yield self.character.env.timeout(remaining_time)

                    if self.character.env.now >= self._buff_end_time:
                        self.deactivate()
                        break

            self.character.env.process(callback(self))
        # else:
        # if self.PRINTS_ACTIVATION:
        # self.character.print(f"{self.name} refreshed")
        # self._buff_end_time = self.character.env.now + self.duration

    def deactivate(self):
        super().deactivate()
        self.character.remove_sp_bonus(self.DMG_BONUS)
