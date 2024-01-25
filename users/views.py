from django.shortcuts import render

from users.models import DndUser, UserCharacter, UserCharacterStat, UserCharacterAbility, \
UserCharacterSavethrow, UserCharacterLanguage, UserCharacterArmorMastery, UserCharacterWeaponMastery, \
UserCharacterInstrumentMastery, UserCharacterSkill

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from pprint import pprint
import os
import base64
import uuid

from .serializers import UserCharacterSerializer

class UserCharacterView(APIView):

    def get(self, request, user_id):
        query = get_object_or_404(DndUser, id=user_id)
        
        if query.email:

            user_characters = [
                {
                    'id': character['id'],
                    'name': character['character_name'],
                    'description': character['character_description'],
                    'avatar': character['character_avatar_id'],
                    'lvl': character['character_level'],
                    'race': character['character_race'],
                    'class': character['character_class'],
                    'background': character['character_background'],
                    'base_armor': character['character_base_armor'],
                    'hit_dice': character['character_hit_dice'],
                    'max_hits': character['character_max_hits'],
                    'initiative': character['character_initiative'],
                    'move_speed': character['character_speed'],
                    'passive_presep': character['character_passive_preseption'],
                    'passive_presep': character['character_passive_preseption'],
                    'worldview': character['character_worldview'],
                    'char_size': character['character_size'],
                    'char_weight': character['character_weight'],

                    'stats': [
                        {
                            'name': ability_obj['name'],
                            'value': ability_obj['value'],
                            'modifer': ability_obj['modifer'],
                        } for ability_obj in UserCharacter.objects.get(id=character['id']).char_stats.all().values()
                    ],
                    'abilities': [
                        {
                            'name': ability_obj['name'],
                            'value': ability_obj['value'],
                            'type': ability_obj['ability_type'],
                        } for ability_obj in UserCharacter.objects.get(id=character['id']).char_abilities.all().values()
                    ],
                    'skills': [
                        {
                            'name': skill_obj['name'],
                        } for skill_obj in UserCharacter.objects.get(id=character['id']).char_skills.all().values()
                    ],
                    'savethrows': [
                        {
                            'name': savethrow['name']
                        } 
                        for savethrow in UserCharacter.objects.get(id=character['id']).char_savethrows.all().values()
                    ],
                    'languages': [
                        {
                            'name': language['name']
                        } 
                        for language in UserCharacter.objects.get(id=character['id']).char_languages.all().values()
                    ],
                    'armor_mastery': [
                        {
                            'name': armor_mastery['name']
                        } 
                        for armor_mastery in UserCharacter.objects.get(id=character['id']).char_armor_mastery.all().values()
                    ],
                    'weapon_mastery': [
                        {
                            'name': weapon_mastery['name']
                        } 
                        for weapon_mastery in UserCharacter.objects.get(id=character['id']).char_weapon_mastery.all().values()
                    ],
                    'instrument_mastery': [
                        {
                            'name': instrument_mastery['name']
                        } 
                        for instrument_mastery in UserCharacter.objects.get(id=character['id']).char_instrument_mastery.all().values()
                    ],

                } for character in query.character.all().values()]
            
            return Response(user_characters, status=status.HTTP_200_OK)
        
        
    def post(self, request, user_id):
        character_data = {
            'character_name': request.data.get('charName'),
            'character_description': request.data.get('charDescription'),
            'character_avatar': request.data.get('charAvatar'),
            'character_level': request.data.get('charLvl'),
            'character_race' : request.data.get('charRace'),
            'character_class':  request.data.get('charClass'),
            'character_skills': request.data.get('charSkills'),
            'character_subclass': 'test false',
            'character_savethrows': request.data.get('charSavethrows'),
            'character_languages': request.data.get('charLanguages'),
            'character_armor_mastery': request.data.get('charArmorMastery'),
            'character_weapon_mastery': request.data.get('charWeaponMastery'),
            'character_instrument_mastery': request.data.get('charInstrumentMastery'),
            'character_background': request.data.get('charBackground'),
            'character_stats': request.data.get('charStats'),
            'character_abilities': request.data.get('charAbilities'),
            'character_armor_class': request.data.get('charArmorClass'),
            'character_max_hits': request.data.get('charMaxHits'),
            'character_hit_dice': request.data.get('charHitDice'),
            'character_initiative': request.data.get('charInitiative'),
            'character_speed': request.data.get('charSpeed'),
            'character_mastery': request.data.get('charMasteryBonuce'),
            'character_passive_preseption': request.data.get('charPassivePresep'),
            'character_worldview': request.data.get('charWorldView'),
            'character_weight': request.data.get('charWeight'),
            'character_size': request.data.get('charSize'),
        }

        created_character, created = UserCharacter.objects.update_or_create(
            dnd_user_id = user_id,
            character_name = character_data['character_name'],
            character_description = character_data['character_description'],
            character_level = character_data['character_level'],
            character_race = character_data['character_race'],
            character_class = character_data['character_class'],
            character_subclass = character_data['character_subclass'],
            character_background = character_data['character_background'],
            character_base_armor = character_data['character_armor_class'],
            character_max_hits = character_data['character_max_hits'],
            character_hit_dice = character_data['character_hit_dice'],
            character_initiative = character_data['character_initiative'],
            character_speed = character_data['character_speed'],
            character_mastery = character_data['character_mastery'],
            character_passive_preseption = character_data['character_passive_preseption'],
            character_worldview = character_data['character_worldview'],
            character_size = character_data['character_size'],
            character_weight = character_data['character_weight'],
        )

        for skill in character_data['character_skills']:
            UserCharacterSkill.objects.update_or_create(character_id=created_character, name=skill['name'])

        for stat in character_data['character_stats']:
            UserCharacterStat.objects.update_or_create(
                character_id=created_character,
                name = stat['statParam'],
                value = int(stat['value']),
                modifer = int(stat['modifer']),
            )
        
        for ability in character_data['character_abilities']:
            UserCharacterAbility.objects.update_or_create(
                character_id=created_character,
                name = ability['name'],
                value = int(ability['value']),
                ability_type = ability['abilityType'],
            )

        for savethrow in character_data['character_savethrows']:
            UserCharacterSavethrow.objects.update_or_create(character_id=created_character, name=savethrow['name'])

        for language in character_data['character_languages']:
            print(language)
            UserCharacterLanguage.objects.update_or_create(character_id=created_character, name=language['name'])

        if len(character_data['character_armor_mastery']) > 0:   
            for armorMastery in character_data['character_armor_mastery']:
                UserCharacterArmorMastery.objects.update_or_create(character_id=created_character, name=armorMastery['name'])

        if len(character_data['character_weapon_mastery']) > 0:   
            for weapon_mastery in character_data['character_weapon_mastery']:
                UserCharacterWeaponMastery.objects.update_or_create(character_id=created_character, name=weapon_mastery['name'])

        if len(character_data['character_instrument_mastery']) > 0:   
            for instrument_mastery in character_data['character_instrument_mastery']:
                UserCharacterInstrumentMastery.objects.update_or_create(character_id=created_character, name=instrument_mastery['name'])

        if character_data['character_avatar']:
            image_folder_path = f'{os.getcwd()}/app_data/{created_character.character_name}_user_id_{user_id}/'

            if not os.path.exists(f'{image_folder_path}'):
                os.mkdir(f'{image_folder_path}')


            avatar_id = uuid.uuid4()
            UserCharacter.objects.filter(id=created_character.id).update(
                character_avatar_id=avatar_id,
                character_avatar_name=character_data['character_avatar']['name'],
                character_avatar_data=character_data['character_avatar']['data'],
                character_avatar_ext=character_data['character_avatar']['ext'],
            )

            image_file = f'{image_folder_path}_{avatar_id}_avatar_{character_data["character_name"]}{character_data["character_avatar"]["ext"]}'
            
            with open(f'{image_file}', 'wb') as file:
                file.write(base64.b64decode(character_data["character_avatar"]['data']))

        return Response(request.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, user_id):
        target_character_id = request.data.get('characterId')
        target_character_name = request.data.get('characterName')
        
        target_character = get_object_or_404(UserCharacter, id=target_character_id, character_name=target_character_name)
        target_character.delete().save()


        return Response({'status': 'ok'}, status=status.HTTP_204_NO_CONTENT)
    

class UserCharacterControl(APIView):

    def get(self, request, user_id, character_id):
        avatar_id = request.GET.get('avatar')
        
        if avatar_id:
            query = get_object_or_404(UserCharacter, character_avatar_id=avatar_id)

        return Response({
            'file_name': query.character_avatar_name,
            'file_data': query.character_avatar_data, 
            'file_ext': query.character_avatar_ext,
            'file_type': 'test',
        })