from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.models import DndUser
from api.models import WeaponItemEquip, ArmorItemEquip, InstrumentItemEquip

class RegisterDndUser(ModelSerializer):

    class Meta(object):
        model = DndUser
        fields = ['username', 'password', 'email',]

class DetailRaceViewSerializer(serializers.Serializer):

    char_race_name = serializers.CharField(max_length=255,)
    subrace_avalible = serializers.BooleanField()
    age = serializers.IntegerField()
    speed = serializers.IntegerField()
    size = serializers.IntegerField()
    weight = serializers.CharField()
    race_description = serializers.CharField()
    book_id = serializers.IntegerField()

    def char_race_name(self, value):
        print(value)

class WeaponItemEquipSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    minDmg = serializers.IntegerField(source='min_dmg')
    maxDmg = serializers.IntegerField(source='max_dmg')
    dmgType = serializers.CharField(max_length=255, source='dmg_type')
    effectiveRange = serializers.IntegerField(source='effective_range')
    maxRange = serializers.IntegerField(source='max_range')
    rangedWeapon = serializers.BooleanField(source='ranged_weapon')
    meleeWeapon = serializers.BooleanField(source='melee_weapon')
    onehanded = serializers.BooleanField()
    twohanded = serializers.BooleanField()
    weight = serializers.IntegerField()
    price = serializers.IntegerField(source='default_price')
    description = serializers.CharField()
    itemType = serializers.CharField(source='item_type')

    class Meta:
        model = WeaponItemEquip
        exclude = ('book_id',)
    
class ArmorItemEquipSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField(source='default_price')
    baseArmor = serializers.IntegerField(source='base_armor')
    dexModif = serializers.IntegerField(source='dex_modif')
    dexModifFull = serializers.BooleanField(source='dex_modif_full')
    sneakPenalty = serializers.BooleanField(source='sneak_penalty')
    lightArmor = serializers.BooleanField(source='light_armor')
    mediumArmor = serializers.BooleanField(source='medium_armor')
    heavyArmor = serializers.BooleanField(source='heavy_armor')
    shield = serializers.BooleanField()
    weight = serializers.IntegerField()
    itemType = serializers.CharField(source='item_type')

    class Meta:
        model = ArmorItemEquip
        exclude = ('book_id',)

class InstrumentItemEquipSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField(source='default_price')
    weight = serializers.IntegerField()
    itemType = serializers.CharField(source='item_type')

    class Meta:
        model = ArmorItemEquip
        exclude = ('book_id',)