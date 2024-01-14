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
    character_level = models.IntegerField()
    character_race = models.CharField(max_length=255)
    character_class = models.CharField(max_length=255)
    character_subclass = models.CharField(null=True, blank=True)
    character_background = models.CharField(max_length=255)
    character_avatar_data = models.TextField(blank=True, null=True)
    character_avatar_name = models.TextField(blank=True, null=True)
    character_avatar_ext = models.CharField(blank=True, null=True)
    character_avatar_id = models.TextField(blank=True, null=True)

    dnd_user = models.ForeignKey(DndUser, on_delete=models.CASCADE, related_name='character')

class UserCharacterStats(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    character_id = models.OneToOneField(UserCharacter, on_delete=models.CASCADE, primary_key=True)

class UserCharacterStatItem(models.Model):
    name = models.CharField(max_length=10)
    value = models.IntegerField()
    modifer = models.IntegerField()

    user_character_stats = models.ForeignKey(UserCharacterStats, on_delete=models.CASCADE, related_name='char_stat')

class UserCharacterAbilities(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    character_id = models.OneToOneField(UserCharacter, on_delete=models.CASCADE, primary_key=True)

class UserCharacterAbilityItem(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()
    ability_type = models.CharField(max_length=10)

    user_character_abilities = models.ForeignKey(UserCharacterAbilities, on_delete=models.CASCADE, related_name='char_abilities')