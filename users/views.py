from django.shortcuts import render

from users.models import DndUser, UserCharacter
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserCharacterSerializer

class UserCharacterView(APIView):

    def get(self, request, user_id):
        query = get_object_or_404(DndUser, id=user_id)

        if query.email:
            return Response('test', status=status.HTTP_200_OK)
        
    def post(self, request, user_id):
        character_data = {
            'character_name': request.data.get('charName')
        }
        print(len(character_data['character_name']))
        char_serializer = UserCharacterSerializer(data=character_data)
        print(char_serializer.is_valid(raise_exception=True))

        return Response(request.data, status=status.HTTP_201_CREATED)
