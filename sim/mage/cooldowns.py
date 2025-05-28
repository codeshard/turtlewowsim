from sim.character import Character
from sim.cooldown import Cooldown
from sim.spell_school import DamageType


class ConeOfColdCooldown(Cooldown):
    PRINTS_ACTIVATION = False

    @property
    def cooldown(self):
        return 10


class FireBlastCooldown(Cooldown):
    PRINTS_ACTIVATION = False

    def __init__(self, character: Character, cooldown: float):
        super().__init__(character)
        self._cd = cooldown

    @property
    def cooldown(self):
        return self._cd


class FrostNovaCooldown(Cooldown):
    PRINTS_ACTIVATION = False

    def __init__(self, character: Character, cooldown: float):
        super().__init__(character)
        self._cd = cooldown
        self._cast_number = 0

    @property
    def cooldown(self):
        return self._cd

    # need special handling for when cooldown ends due to possibility of cooldown reset # noqa E501
    def activate(self):
        if self.usable:
            self._active = True

            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} activated")

            cooldown = self.cooldown
            if self.STARTS_CD_ON_ACTIVATION and cooldown:
                self._on_cooldown = True

                def callback(self, cooldown, cast_number):
                    yield self.env.timeout(cooldown)
                    # if cooldown got reset already, do nothing
                    if cast_number == self._cast_number:
                        if self.PRINTS_ACTIVATION:
                            self.character.print(
                                f"{self.name} cooldown ended after {cooldown} seconds"  # noqa E501
                            )

                        self._on_cooldown = False
                        self._cast_number += 1

                self.character.env.process(
                    callback(self, cooldown, self._cast_number)
                )

            if self.duration:

                def callback(self):
                    yield self.character.env.timeout(self.duration)
                    self.deactivate()

                self.character.env.process(callback(self))
            else:
                self.deactivate()

    def reset_cooldown(self):
        if self.PRINTS_ACTIVATION:
            self.character.print(f"{self.name} cooldown reset")
        self._cast_number += 1
        self._on_cooldown = False


class ColdSnapCooldown(Cooldown):
    PRINTS_ACTIVATION = False

    @property
    def cooldown(self):
        return 600

    def activate(self):
        if self.usable:
            super().activate()
            # reset all frost cooldowns (only frost nova for now)
            if hasattr(self.character, "frost_nova_cd"):
                self.character.frost_nova_cd.reset_cooldown()


class IciclesCooldown(Cooldown):
    PRINTS_ACTIVATION = False

    @property
    def cooldown(self):
        return 30

    @property
    def usable(self):
        return not self._active and not self._on_cooldown

    def deactivate(self):
        self._active = False
        if self.PRINTS_ACTIVATION:
            self.character.print(f"{self.name} deactivated")

        if self.cooldown:
            self._on_cooldown = True

            self._time_off_cooldown = self.env.now + self.cooldown

            def callback(self):
                yield self.env.timeout(self.cooldown)

                # flash freeze can proc and restart the cooldown,
                # need to check the latest _time_off_cooldown for this thread
                if self._time_off_cooldown <= self.env.now:
                    self._on_cooldown = False

            self.character.env.process(callback(self))


class ArcaneSurgeCooldown(Cooldown):
    # requires partial resist as well
    PRINTS_ACTIVATION = False

    def __init__(self, character: Character, apply_cd_haste: bool):
        super().__init__(character)
        self._base_cd = 8
        self._resist_time = None
        self._apply_cd_haste = apply_cd_haste

    @property
    def cooldown(self):
        return (
            self._base_cd
            / self.character.get_haste_factor_for_damage_type(
                DamageType.ARCANE
            )
            if self._apply_cd_haste
            else self._base_cd
        )

    def enable_due_to_resist(self):
        self._resist_time = self.character.env.now

    @property
    def usable(self):
        if not self._active and not self._on_cooldown and self._resist_time:
            if self.character.env.now - self._resist_time < 4:
                return True
            else:
                self._resist_time = None

        return False

    def time_left(self):
        if self._resist_time:
            return self._resist_time + 3 - self.character.env.now
        return 0

    def activate(self):
        super().activate()
        self._resist_time = None


class ArcaneRuptureCooldown(Cooldown):
    PRINTS_ACTIVATION = False
    TRACK_UPTIME = True

    def __init__(self, character: Character, apply_cd_haste: bool):
        super().__init__(character)
        self._base_cd = 15
        self._apply_cd_haste = apply_cd_haste
        self._cast_number = 0

    @property
    def usable(self):
        return not self._on_cooldown

    @property
    def duration(self):
        return 8

    @property
    def cooldown(self):
        return (
            self._base_cd
            / self.character.get_haste_factor_for_damage_type(
                DamageType.ARCANE
            )
            if self._apply_cd_haste
            else self._base_cd
        )

    # need special handling for when cooldown ends due to possibility of cooldown reset # noqa E501
    def activate(self):
        if self.usable:
            self._active = True

            self.track_buff_start_time()

            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} activated")

            cooldown = self.cooldown
            if self.STARTS_CD_ON_ACTIVATION and cooldown:
                self._on_cooldown = True

                def callback(self, cooldown, cast_number):
                    yield self.env.timeout(cooldown)
                    # if cooldown got reset already, do nothing
                    if cast_number == self._cast_number:
                        if self.PRINTS_ACTIVATION:
                            self.character.print(
                                f"{self.name} cooldown ended after {cooldown} seconds"  # noqa E501
                            )

                        self._on_cooldown = False
                        self._cast_number += 1

                self.character.env.process(
                    callback(self, cooldown, self._cast_number)
                )

            if self.duration:

                def callback(self):
                    yield self.character.env.timeout(self.duration)
                    self.deactivate()

                self.character.env.process(callback(self))
            else:
                self.deactivate()

    def reset_cooldown(self):
        if self.PRINTS_ACTIVATION:
            self.character.print(f"{self.name} cooldown reset")
        self._cast_number += 1
        self._on_cooldown = False


class TemporalConvergenceCooldown(Cooldown):
    PRINTS_ACTIVATION = False

    @property
    def cooldown(self):
        return 15


class Combustion(Cooldown):
    STARTS_CD_ON_ACTIVATION = False

    def __init__(self, character: Character):
        super().__init__(character)
        self._charges = 0
        self._crit_bonus = 0

    @property
    def cooldown(self):
        return 180

    @property
    def crit_bonus(self):
        return self._crit_bonus

    def use_charge(self):
        if self._charges:
            self._charges -= 1
            if self._charges == 0:
                self.deactivate()

    def cast_fire_spell(self):
        if self._charges:
            self._crit_bonus += 10

    def activate(self):
        super().activate()
        self._charges = 3
        self._crit_bonus = 10


class PresenceOfMind(Cooldown):
    STARTS_CD_ON_ACTIVATION = False

    def __init__(self, character: Character, apply_cd_haste: bool):
        super().__init__(character)
        self._base_cd = 180
        self._apply_cd_haste = apply_cd_haste

    @property
    def cooldown(self):
        return (
            self._base_cd
            / self.character.get_haste_factor_for_damage_type(
                DamageType.ARCANE
            )
            if self._apply_cd_haste
            else self._base_cd
        )

    @property
    def duration(self):
        return 9999


class ArcanePower(Cooldown):
    def __init__(self, character: Character, apply_cd_haste: bool):
        super().__init__(character)
        self._base_cd = 180
        self._apply_cd_haste = apply_cd_haste

    @property
    def cooldown(self):
        return (
            self._base_cd
            / self.character.get_haste_factor_for_damage_type(
                DamageType.ARCANE
            )
            if self._apply_cd_haste
            else self._base_cd
        )

    @property
    def duration(self):
        return 20

    def activate(self):
        super().activate()
        self.character.add_cooldown_haste(self.name, 30)

    def deactivate(self):
        super().deactivate()
        self.character.remove_cooldown_haste(self.name)
