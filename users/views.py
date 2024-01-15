from django.shortcuts import render

from users.models import DndUser, UserCharacter, UserCharacterStats, UserCharacterStatItem, UserCharacterAbilities, UserCharacterAbilityItem
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
                    'stats': [
                        {
                        'name': statObj['name'],
                        'value': statObj['value'],
                        'modifer': statObj['modifer'],

                        }
                        for statObj in UserCharacterStats.objects.get(character_id=character['id']).char_stat.all().values()
                    ],
                    'abilities': [
                        {
                        'name': ability_obj['name'],
                        'value': ability_obj['value'],
                        'type': ability_obj['ability_type'],

                        }
                        for ability_obj in UserCharacterAbilities.objects.get(character_id=character['id']).char_abilities.all().values()
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
            'character_subclass': 'test false',
            'character_background': request.data.get('charBackground'),
            'character_stats': request.data.get('charStats'),
            'character_abilities': request.data.get('charAbilities'),
        }

        created_character, created = UserCharacter.objects.update_or_create(
            dnd_user_id=user_id,
            character_name=character_data['character_name'],
            character_description=character_data['character_description'],
            character_level=character_data['character_level'],
            character_race=character_data['character_race'],
            character_class=character_data['character_class'],
            character_subclass=character_data['character_subclass'],
            character_background=character_data['character_background'],
        )

        UserCharacterStats.objects.update_or_create(name=character_data['character_name'], character_id=created_character)
        UserCharacterAbilities.objects.update_or_create(name=character_data['character_name'], character_id=created_character)

        char_stats = UserCharacterStats.objects.get(character_id=created_character.id)
        char_abilities = UserCharacterAbilities.objects.get(character_id=created_character.id)

        for stat_obj in character_data['character_stats']:
            UserCharacterStatItem.objects.update_or_create(
                name = stat_obj['statParam'],
                value = int(stat_obj['value']),
                modifer = int(stat_obj['modifer']),

                user_character_stats = char_stats,
            )

        for ability_obj in character_data['character_abilities']:
            UserCharacterAbilityItem.objects.update_or_create(
                name = ability_obj['name'],
                value = int(ability_obj['value']),
                ability_type = ability_obj['abilityType'],

                user_character_abilities = char_abilities,
            )

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