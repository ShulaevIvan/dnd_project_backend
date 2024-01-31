from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import DndUser
from .models import UserCharacter
from api.models import SpellItem


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


class UserCharacterSpellSerializer(ModelSerializer):
    spellTarget = serializers.CharField(source='spell_target')
    spellType = serializers.CharField(source='spell_type')
    bonuceAction = serializers.BooleanField(source='bonuce_action')
    duratationValue = serializers.CharField(source='duratation_value')
    spellLevel = serializers.IntegerField(source='spell_level')
    actionCost = serializers.IntegerField(source='action_cost')

    class Meta(object):
        model = SpellItem
        exclude = [
            'spellbook_id', 
            'spell_type', 
            'spell_target', 
            'bonuce_action', 
            'duratation_value', 
            'action_cost',
            'spell_level',
        ]
