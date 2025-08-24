from turtlewowsim.character import Character
from turtlewowsim.cooldowns import (
    BindingsOfContainedMagicBuff,
    EndlessGulchBuff,
    TrueBandOfSulfurasBuff,
    WrathOfCenariusBuff,
)
from turtlewowsim.env import Environment
from turtlewowsim.equipped_items import EquippedItems
from turtlewowsim.item_procs import (
    BindingsOfContainedMagic,
    BladeOfEternalDarkness,
    EndlessGulch,
    OrnateBloodstoneDagger,
    TrueBandOfSulfuras,
    UnceasingFrost,
    WrathOfCenarius,
)
from turtlewowsim.spell import SPELL_COEFFICIENTS, Spell
from turtlewowsim.spell_school import DamageType


class ItemProcHandler:
    def __init__(
        self,
        character: Character,
        env: Environment,
        equipped_items: EquippedItems,
    ):
        self.character = character
        self.env = env

        self.procs = []

        self.wrath_of_cenarius_buff = None
        self.endless_gulch_buff = None
        self.true_band_of_sulfuras_buff = None
        self.bindings_buff = None

        self.wisdom_of_the_makaru_stacks = 0

        if equipped_items:
            if equipped_items.blade_of_eternal_darkness:
                self.procs.append(
                    BladeOfEternalDarkness(
                        character, self._blade_of_eternal_darkness_proc
                    )
                )
            if equipped_items.ornate_bloodstone_dagger:
                self.procs.append(
                    OrnateBloodstoneDagger(
                        character, self._ornate_bloodstone_dagger_proc
                    )
                )
            if equipped_items.wrath_of_cenarius:
                self.wrath_of_cenarius_buff = WrathOfCenariusBuff(character)
                self.procs.append(
                    WrathOfCenarius(character, self._wrath_of_cenarius_proc)
                )
            if equipped_items.true_band_of_sulfuras:
                self.true_band_of_sulfuras_buff = TrueBandOfSulfurasBuff(
                    character
                )
                self.procs.append(
                    TrueBandOfSulfuras(
                        character, self._true_band_of_sulfuras_proc
                    )
                )
            if equipped_items.endless_gulch:
                self.endless_gulch_buff = EndlessGulchBuff(character)
                self.procs.append(
                    EndlessGulch(character, self._endless_gulch_proc)
                )
            if equipped_items.unceasing_frost:
                self.procs.append(
                    UnceasingFrost(character, self._unceasing_frost_proc)
                )
            if equipped_items.bindings_of_contained_magic:
                self.bindings_buff = BindingsOfContainedMagicBuff(character)
                self.procs.append(
                    BindingsOfContainedMagic(character, self._bindings_proc)
                )

    def check_for_procs(
        self, current_time, spell: Spell, damage_type: DamageType
    ):
        for proc in self.procs:
            proc.check_for_proc(
                current_time, self.env.num_mobs, spell, damage_type
            )

    def _tigger_proc_dmg(self, spell, min_dmg, max_dmg, damage_type):
        dmg = self.character.roll_spell_dmg(
            min_dmg, max_dmg, SPELL_COEFFICIENTS.get(spell, 0), damage_type
        )
        dmg = self.character.modify_dmg(dmg, damage_type, is_periodic=False)

        partial_amount = self.character.roll_partial(
            is_dot=False, is_binary=False
        )
        if partial_amount < 1:
            dmg = int(dmg * partial_amount)

        self.env.meter.register_proc_dmg(
            char_name=self.character.name,
            spell_name=spell.value,
            dmg=dmg,
            aoe=False,
        )

    def _blade_of_eternal_darkness_proc(self):
        self._tigger_proc_dmg(
            Spell.ENGULFING_SHADOWS, 100, 100, DamageType.SHADOW
        )

    def _ornate_bloodstone_dagger_proc(self):
        self._tigger_proc_dmg(Spell.BURNING_HATRED, 250, 250, DamageType.FIRE)

    def _wrath_of_cenarius_proc(self):
        if self.wrath_of_cenarius_buff:
            self.wrath_of_cenarius_buff.activate()

    def _endless_gulch_proc(self):
        self.wisdom_of_the_makaru_stacks += 1
        self.character.print(
            f"Wisdom of the Makaru proc {self.wisdom_of_the_makaru_stacks}"
        )
        if self.wisdom_of_the_makaru_stacks >= 10:
            self.wisdom_of_the_makaru_stacks = 0
            if self.endless_gulch_buff:
                self.endless_gulch_buff.activate()

    def _true_band_of_sulfuras_proc(self):
        if self.true_band_of_sulfuras_buff:
            self.true_band_of_sulfuras_buff.activate()

    def _unceasing_frost_proc(self):
        self.env.debuffs.add_freezing_cold()

    def _bindings_proc(self):
        if self.bindings_buff:
            self.bindings_buff.activate()
