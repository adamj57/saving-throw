from django.contrib import admin
from mdb import models


@admin.register(models.Background)
class BackgroundAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BasicAbility)
class BasicAbilityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CharacterSheet)
class CharacterSheetAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CharacterSheetAbilityData)
class CharacterSheetAbilityDataAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CharacterSheetClassData)
class CharacterSheetClassDataAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CharacterSheetSpellData)
class CharacterSheetSpellDataAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CharacterSheetSpellSlotData)
class CharacterSheetSpellSlotDataAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Class)
class ClassAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Dice)
class DiceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EquipmentItem)
class EquipmentItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Race)
class RaceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SkillSkeleton)
class SkillSkeletonAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Spell)
class SpellAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SpellType)
class SpellTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TextAbility)
class TextAbilityAdmin(admin.ModelAdmin):
    pass
