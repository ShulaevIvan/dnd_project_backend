from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import DndUser
from .models import UserCharacter


class UserCharacterSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserCharacter
        exclude = [
            'id',
            'character_description',
            'character_avatar',
            'character_level',
            'character_race',
            'character_class',
            'character_subclass',
            'character_background',
            'dnd_user',
        ]

    def validate_character_name(self, value):
        if value == '' or len(value) < 3:
            raise serializers.ValidationError("Email cannot be empty.", code="invalid")
        
        return super().validate(value)
