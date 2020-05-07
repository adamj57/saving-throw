from math import floor

from django.contrib.auth.models import User
from django.db import models

from mdb.fields import AbilityValueField, DurationField
from sheet.sheet_attributes import Skill


class ModelNameMixin:
    def __str__(self):
        return self.name


class BasicAbility(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=32)

    def short(self):
        return self.name[:3].upper()

    class Meta:
        verbose_name = "Basic Ability"
        verbose_name_plural = "Basic Abilities"


class SkillSkeleton(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=32)
    base_ability = models.ForeignKey(BasicAbility, on_delete=models.SET_NULL, null=True, verbose_name="Base ability")

    class Meta:
        verbose_name_plural = "Skills"


class Dice(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=64)
    sides = models.IntegerField(verbose_name="Sides")

    def avg_roll(self):
        return (1 + self.sides) / 2

    class Meta:
        verbose_name_plural = "Dice"


class Language(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=32)


class Size(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=16)


class TextAbility(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=64)
    desc = models.TextField(verbose_name="Description")


class Race(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=32)
    speed = models.IntegerField(verbose_name="Speed")
    abilities = models.ManyToManyField(TextAbility)
    languages = models.ManyToManyField(Language)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)


class Background(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=32)
    feature = models.TextField(verbose_name="Feature description")


class ItemType(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=32)
    equipable_attack = models.BooleanField(verbose_name="Equipable for attack")
    equipable_defense = models.BooleanField(verbose_name="Equipable for defense")
    consumable = models.BooleanField(verbose_name="Consumable")


class Item(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=128)
    desc = models.TextField(verbose_name="Description")
    type = models.ForeignKey(ItemType, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(verbose_name="Price")


class SpellType(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=32)


class Spell(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=64)
    level = models.IntegerField(verbose_name="Level")
    casting_time = DurationField(verbose_name="Casting time")
    duration = models.TimeField(verbose_name="Duration")
    v_component = models.BooleanField(verbose_name="Verbal")
    s_component = models.BooleanField(verbose_name="Somatic")
    m_component = models.CharField(verbose_name="Material", null=True, max_length=128)
    range = models.IntegerField(verbose_name="Range")
    desc = models.TextField(verbose_name="Description")
    ritual = models.BooleanField(verbose_name="Ritual")
    type = models.ForeignKey(SpellType, on_delete=models.SET_NULL, null=True)


class StatusEffect(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=64)


class CharacterSheet(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Character name", max_length=64)

    skill_prof = models.ManyToManyField(SkillSkeleton, verbose_name="Skill proficiencies", related_name="skill_prof")
    skill_expert = models.ManyToManyField(SkillSkeleton, verbose_name="Skill expertises", related_name="skill_expert")

    race = models.ForeignKey(Race, on_delete=models.SET_NULL, null=True)
    background = models.ForeignKey(Background, on_delete=models.SET_NULL, null=True)

    current_hp = models.IntegerField(verbose_name="Current HP")

    temp_hp = models.IntegerField(verbose_name="Temporary HP")
    temp_hp_reason = models.IntegerField(verbose_name="Reason for temporary HP")

    inspiration = models.BooleanField(verbose_name="Inspiration")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="character_sheets")

    def level(self):
        return sum((class_data.level for class_data in self.class_data.all()))

    def ability_data(self, name):
        name = name.capitalize()

        return self.abilities_data.filter(ability__name__startswith=name).first()

    def proficiency_bonus(self):
        level = self.level()

        prof = floor((level - 1) / 4) + 2  # that's pretty neat
        return min(prof, 6)

    def hit_dice(self):
        return self.class_data.all() \
            .values_list("cls__hit_dice", "level", named=True) \
            .order_by("cls__hit_dice__sides")

    def max_hp(self):
        vals = self.class_data.all().values_list("cls__hit_dice", "level")
        con = self.ability_data("CON").value.real_value()

        hp = 0
        hit_dice: Dice
        for hit_dice, level in vals:
            first_lvl_hp = hit_dice.sides + con
            next_lvls_hp = (level - 1) * (hit_dice.avg_roll() + con)
            hp += first_lvl_hp + next_lvls_hp

        return hp

    def skills(self):
        for skill in SkillSkeleton.objects.all().order_by("name"):
            ability_data = self.abilities_data.filter(ability=skill.base_ability).first()
            yield Skill(name=skill.name,
                        ability_data=ability_data,
                        prof=skill in self.skill_prof.all(),
                        expert=skill in self.skill_expert.all())

    def spell_save_dc(self, cls=None):
        atck_mod = self.spell_atack_modifier(cls=cls)
        if atck_mod is None:
            return None
        else:
            return 8 + atck_mod

    def spell_atack_modifier(self, cls=None):
        spellcaster_clasess = self.class_data.filter(
            cls__spellcasting_ability__isnull=False)  # TODO: Create QS for that

        if cls is not None:
            cls_instance: Class
            cls_instance = self.class_data.filter(cls=cls)

            if cls_instance:
                return self.proficiency_bonus() + cls_instance.spellcasting_modifier(self)
            else:
                # TODO: Napisać wyjątek
                return None  # Tymczasowo!

        elif spellcaster_clasess.count() == 1:
            cls_instance: Class
            cls_instance = spellcaster_clasess.first()

            return self.proficiency_bonus() + cls_instance.spellcasting_modifier(self)
        else:
            # TODO: Napisać wyjątek
            return None  # Tymczasowo!


class StatusEffectData(models.Model):
    effect = models.ForeignKey(StatusEffect, on_delete=models.CASCADE)
    duration = DurationField(verbose_name="Duration")
    character_sheet = models.ForeignKey(CharacterSheet, on_delete=models.CASCADE, related_name="status_effects_data")


class Class(ModelNameMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=64)
    hit_dice = models.ForeignKey(Dice, on_delete=models.SET_NULL, null=True, verbose_name="Hit dice")
    saving_throw_prof = models.ManyToManyField(BasicAbility,
                                               verbose_name="Saving throw profficiences",
                                               related_name="class_using_as_saving_throw_proficiency")
    spellcasting_ability = models.ForeignKey(BasicAbility, on_delete=models.SET_NULL, null=True)

    def start_hp(self):
        return self.hit_dice.sides

    def spellcasting_modifier(self, character_sheet: CharacterSheet):
        if self.spellcasting_ability is not None:
            ability_name = self.spellcasting_ability.name
            ability_data: CharacterSheetAbilityData
            ability_data = character_sheet.ability_data(ability_name)
            return ability_data.value.modifier()
        else:
            raise ValueError("This class doesn't possess spellcasting ability!")

    class Meta:
        verbose_name_plural = "Classes"


class EquipmentItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Quantity")
    equipped = models.BooleanField(verbose_name="Equipped")
    additional_info = models.TextField(verbose_name="Additional info")
    character_sheet = models.ForeignKey(CharacterSheet,
                                        on_delete=models.CASCADE,
                                        verbose_name="Character Sheet",
                                        related_name="equipment_items")

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("item", "character_sheet"), name="one_unique_item_per_sheet"),
        )


class CharacterSheetSpellData(models.Model):
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    prepared = models.BooleanField(verbose_name="Prepared")
    character_sheet = models.ForeignKey(CharacterSheet,
                                        on_delete=models.CASCADE,
                                        verbose_name="Character Sheet",
                                        related_name="spell_data")

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("spell", "character_sheet"), name="one_unique_spell_per_sheet"),
        )


class CharacterSheetClassData(models.Model):
    cls = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, verbose_name="Class")
    level = models.IntegerField(verbose_name="Level")
    character_sheet = models.ForeignKey(CharacterSheet,
                                        on_delete=models.CASCADE,
                                        verbose_name="Character Sheet",
                                        related_name="class_data")

    class Meta:
        verbose_name = "Character Sheet Class Data"
        verbose_name_plural = "Character Sheet Class Data"
        constraints = (
            models.UniqueConstraint(fields=("cls", "character_sheet"), name="one_unique_class_per_sheet"),
        )


class CharacterSheetAbilityData(models.Model):
    ability = models.ForeignKey(BasicAbility, on_delete=models.SET_NULL, null=True)
    value = AbilityValueField(verbose_name="Value")
    character_sheet = models.ForeignKey(CharacterSheet,
                                        on_delete=models.CASCADE,
                                        verbose_name="Character Sheet",
                                        related_name="abilities_data")

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("ability", "character_sheet"), name="one_unique_ability_per_sheet"),
        )


class CharacterSheetSpellSlotData(models.Model):
    level = models.IntegerField(verbose_name="Level")
    quantity = models.IntegerField(verbose_name="Quantity")
    character_sheet = models.ForeignKey(CharacterSheet,
                                        on_delete=models.CASCADE,
                                        verbose_name="Character Sheet",
                                        related_name="spell_slot_data")

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("level", "character_sheet"), name="one_unique_level_per_sheet"),
        )
