from django.shortcuts import render

from users.models import DndUser, UserCharacter
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from pprint import pprint

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
                    'avatar': character['character_avatar'],
                    'lvl': character['character_level'],
                    'race': character['character_race'],
                    'class': character['character_class'],
                    'background': character['character_background'],
                    
                } for character in query.character.all().values()]
            
            return Response(user_characters, status=status.HTTP_200_OK)
        
    def post(self, request, user_id):
        character_data = {
            'character_name': request.data.get('charName'),
            'character_description': request.data.get('charDescription'),
            'character_avatar': 'test',
            'character_level': request.data.get('charLvl'),
            'character_race' : request.data.get('charRace'),
            'character_class':  request.data.get('charClass'),
            'character_subclass': 'test false',
            'character_background': request.data.get('charBackground')
        }
        query = UserCharacter.objects.get_or_create(
            dnd_user_id=user_id,
            character_name=character_data['character_name'],
            character_description=character_data['character_description'],
            character_avatar=character_data['character_avatar'],
            character_level=character_data['character_level'],
            character_race=character_data['character_race'],
            character_class=character_data['character_class'],
            character_subclass=character_data['character_subclass'],
            character_background=character_data['character_background'],
        )
        # char_serializer = UserCharacterSerializer(data=character_data, many=True)
        # print(char_serializer.is_valid(raise_exception=True))

        return Response(request.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, user_id):
        target_character_id = request.data.get('characterId')
        target_character_name = request.data.get('characterName')
        
        target_character = get_object_or_404(UserCharacter, id=target_character_id, character_name=target_character_name)
        target_character.delete().save()


        return Response({'status': 'ok'}, status=status.HTTP_204_NO_CONTENT)
