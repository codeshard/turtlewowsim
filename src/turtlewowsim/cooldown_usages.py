from dataclasses import dataclass


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
