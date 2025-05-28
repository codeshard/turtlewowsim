from dataclasses import dataclass

from sim.cooldown import (
    Berserking,
    BloodFury,
    CharmOfMagic,
    MindQuickeningGem,
    Perception,
    PotionOfQuickness,
    RestrainedEssenceofSapphiron,
    TalismanofEphemeralPower,
    ZandalarianHeroCharm,
)
from sim.mage import ArcanePower, Combustion, PresenceOfMind


class Cooldowns:
    def __init__(self, character):
        # mage cds
        has_accelerated_arcana = False
        if hasattr(character.tal, "accelerated_arcana"):
            has_accelerated_arcana = character.tal.accelerated_arcana

        self.combustion = Combustion(character)
        self.arcane_power = ArcanePower(character, has_accelerated_arcana)
        self.presence_of_mind = PresenceOfMind(
            character, has_accelerated_arcana
        )

        self.potion_of_quickness = PotionOfQuickness(character)

        self.charm_of_magic = CharmOfMagic(character)
        self.toep = TalismanofEphemeralPower(character)
        self.reos = RestrainedEssenceofSapphiron(character)
        self.mqg = MindQuickeningGem(character)
        self.zhc = ZandalarianHeroCharm(character)

        # racials
        self.berserking15 = Berserking(character, 15)
        self.berserking10 = Berserking(character, 10)
        self.blood_fury = BloodFury(character)
        self.perception = Perception(character)


@dataclass(kw_only=True)
class CooldownUsages:
    # Mage
    combustion: float | list[float] | None = None
    arcane_power: float | list[float] | None = None
    presence_of_mind: float | list[float] | None = None

    # Consumables
    potion_of_quickness: float | list[float] | None = None

    # Racials
    berserking15: float | list[float] | None = None
    berserking10: float | list[float] | None = None
    blood_fury: float | list[float] | None = None
    perception: float | list[float] | None = None

    # Trinkets
    charm_of_magic: float | list[float] | None = None
    toep: float | list[float] | None = None
    zhc: float | list[float] | None = None
    mqg: float | list[float] | None = None
    reos: float | list[float] | None = None
