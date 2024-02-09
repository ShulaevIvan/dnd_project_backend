from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class DndUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(('email address'), unique=True)
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'


class UserCharacter(models.Model):
    character_name = models.CharField(max_length=255)
    character_description = models.TextField(max_length = 30000, blank=True, null=True)
    character_age = models.IntegerField(null=True, blank=True)
    character_level = models.IntegerField()
    character_race = models.CharField(max_length=255)
    character_class = models.CharField(max_length=255)
    character_base_armor = models.IntegerField()
    character_max_hits = models.IntegerField()
    character_hit_dice = models.CharField(max_length=255)
    character_initiative = models.IntegerField()
    character_speed = models.IntegerField()
    character_mastery = models.IntegerField()
    character_passive_preseption = models.IntegerField()
    character_subclass = models.CharField(null=True, blank=True)
    character_background = models.CharField(max_length=255)
    character_avatar_data = models.TextField(null=True, blank=True)
    character_avatar_name = models.TextField(null=True, blank=True)
    character_avatar_ext = models.CharField(null=True, blank=True)
    character_avatar_id = models.TextField(null=True, blank=True)
    character_worldview = models.TextField(null=True, blank=True)
    character_weight = models.CharField(null=True, blank=True, max_length=255)
    character_size = models.IntegerField(null=True, blank=True)

    character_created_time = models.DateTimeField(auto_now_add=True, editable=False)
    character_modifed_time = models.DateTimeField(null=True, blank=True)

    dnd_user = models.ForeignKey(DndUser, on_delete=models.CASCADE, related_name='character')

class UserCharacterSubclass(models.Model):
    name = models.CharField(max_length=255)
    subclass_id = models.IntegerField()

    character_id = models.ForeignKey(UserCharacter, on_delete=models.CASCADE, related_name='char_subclasses')

class UserCharacterStat(models.Model):
    name = models.CharField(max_length=10)
    value = models.IntegerField()
    modifer = models.IntegerField()

    character_id = models.ForeignKey(UserCharacter, on_delete=models.CASCADE, related_name='char_stats')

class UserCharacterAbility(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()
    ability_type = models.CharField(max_length=10)

    character_id = models.ForeignKey(UserCharacter, on_delete=models.CASCADE, related_name='char_abilities')

class UserCharacterSkill(models.Model):
    name = models.CharField(max_length=255)
    skill_data = models.TextField(blank=True, null=True)
    skill_type = models.CharField(max_length=255, null=True, blank=True)

    character_id = models.ForeignKey(UserCharacter, on_delete=models.CASCADE, related_name='char_skills')

class UserCharacterSpell(models.Model):
    spell_id = models.IntegerField()

    character_id = models.ForeignKey(UserCharacter, on_delete=models.CASCADE, related_name='char_spells')

class UserCharacterSavethrow(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    character_id = models.ForeignKey(UserCharacter, on_delete=models.CASCADE, related_name='char_savethrows')

class UserCharacterLanguage(models.Model):
    name = models.CharField(max_length=255)

    character_id = models.ForeignKey(UserCharacter, on_delete=models.CASCADE, related_name='char_languages')

class UserCharacterArmorMastery(models.Model):
    name = models.CharField(max_length=255)

    character_id = models.ForeignKey(UserCharacter, on_delete=models.CASCADE, related_name='char_armor_mastery')

class UserCharacterWeaponMastery(models.Model):
    name = models.CharField(max_length=255)

    character_id = models.ForeignKey(UserCharacter, on_delete=models.CASCADE, related_name='char_weapon_mastery')

class UserCharacterInstrumentMastery(models.Model):
    name = models.CharField(max_length=255)

    character_id = models.ForeignKey(UserCharacter, on_delete=models.CASCADE, related_name='char_instrument_mastery')

class UserCharacterInventory(models.Model):
    items = models.ManyToManyField('CharacterInventoryItem', through='UserCharacterInventoryItem')

    character_id = models.OneToOneField(UserCharacter, on_delete=models.CASCADE, primary_key=True, related_name='char_inventory')

class UserCharacterInventroryMoney(models.Model):
    gold = models.IntegerField(null=True, blank=True)
    silver = models.IntegerField(null=True, blank=True)
    bronze = models.IntegerField(null=True, blank=True)

    inventory_id = models.OneToOneField(UserCharacterInventory, on_delete=models.CASCADE, primary_key=True, related_name='money')

class CharacterInventoryItem(models.Model):
    name = models.CharField(max_length=255)
    item_type =models.CharField(null=True, blank=True)

class UserCharacterInventoryItem(models.Model):
    quantity = models.IntegerField()

    item_id = models.ForeignKey(CharacterInventoryItem, on_delete=models.CASCADE, related_name='character_inventory_item')
    character_id = models.ForeignKey(UserCharacterInventory, on_delete=models.CASCADE, related_name='character_inventory_item')
