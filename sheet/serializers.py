from rest_framework import serializers

from mdb import models


class BasicAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BasicAbility
        fields = "__all__"


class SkillSkeletonSerializer(serializers.ModelSerializer):
    base_ability = BasicAbilitySerializer()

    class Meta:
        model = models.SkillSkeleton
        fields = "__all__"


class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Background
        fields = "__all__"


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Size
        fields = "__all__"


class TextAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TextAbility
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = "__all__"


class RaceSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    abilities = TextAbilitySerializer(many=True)
    languages = LanguageSerializer(many=True)

    class Meta:
        model = models.Race
        fields = "__all__"


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItemType
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    type = ItemTypeSerializer()

    class Meta:
        model = models.Item
        fields = "__all__"


class EquipmentItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = models.EquipmentItem
        exclude = ("character_sheet",)


class SpellTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpellType
        fields = "__all__"


class SpellSerializer(serializers.ModelSerializer):
    type = SpellTypeSerializer()

    class Meta:
        model = models.Spell
        fields = "__all__"


class CharacterSheetSpellDataSerializer(serializers.ModelSerializer):
    spell = SpellSerializer()

    class Meta:
        model = models.CharacterSheetSpellData
        exclude = ("character_sheet",)


class DiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dice
        fields = "__all__"


class ClassSerializer(serializers.ModelSerializer):
    spellcasting_ability = BasicAbilitySerializer()
    saving_throw_prof = BasicAbilitySerializer(many=True)
    hit_dice = DiceSerializer()

    class Meta:
        model = models.Class
        fields = "__all__"


class CharacterSheetClassDataSerializer(serializers.ModelSerializer):
    cls = ClassSerializer()

    class Meta:
        model = models.CharacterSheetClassData
        exclude = ("character_sheet",)


class CharacterSheetAbilityDataSerializer(serializers.ModelSerializer):
    ability = BasicAbilitySerializer()

    # value = SOMESERIALIZER()

    class Meta:
        model = models.CharacterSheetAbilityData
        exclude = ("character_sheet",)


class CharacterSheetSpellSlotDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CharacterSheetSpellSlotData
        exclude = ("character_sheet",)


class CharacterSheetSerializer(serializers.ModelSerializer):
    skill_prof = SkillSkeletonSerializer(many=True)
    skill_expert = SkillSkeletonSerializer(many=True)

    equipment_items = EquipmentItemSerializer(many=True)

    spell_data = CharacterSheetSpellDataSerializer(many=True)
    class_data = CharacterSheetClassDataSerializer(many=True)
    ability_data = CharacterSheetAbilityDataSerializer(many=True)
    spell_slot_data = CharacterSheetSpellSlotDataSerializer(many=True)

    background = BackgroundSerializer()
    race = RaceSerializer()

    class Meta:
        model = models.CharacterSheet
        exclude = ("owner",)
