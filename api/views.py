from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterDndUser
from users.models import DndUser

# Create your views here.

class UserRegisterView(APIView):
    
    def get(self, request):
        print(request)
        return Response('test')
    
    def post(self, request):
        register_data = {
            "username": request.data.get('login'),
            'password': request.data.get('userPassword'),
            'email': request.data.get('email'),
        }
        serializer =  RegisterDndUser(data=register_data)
        return Response('post test')