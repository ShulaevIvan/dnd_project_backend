from django.shortcuts import render

from users.models import DndUser, UserCharacter
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class UserCharacterView(APIView):

    def get(self, request, user_id):
        query = get_object_or_404(DndUser, id=user_id)

        if query.email:
            return Response('test', status=status.HTTP_200_OK)
        
    def post(self, request, user_id):
        print(request.data)

        return Response(request.data, status=status.HTTP_201_CREATED)
