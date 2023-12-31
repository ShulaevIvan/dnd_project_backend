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
    character_avatar = models.TextField(blank=True, null=True)
    character_level = models.IntegerField()
    character_race = models.CharField(max_length=255)
    character_class = models.CharField(max_length=255)
    character_subclass = models.CharField(null=True, blank=True)
    character_background = models.CharField(max_length=255)
    
    dnd_user = models.ForeignKey(DndUser, on_delete=models.CASCADE, related_name='character')

class UserCharacterClass(models.Model):
    name = models.CharField(max_length=255)
    class_level = models.IntegerField()

    user_character_id = models.ForeignKey(UserCharacter, on_delete=models.CASCADE, related_name='user_character_class')