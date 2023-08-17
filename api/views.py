from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

import secrets

from .serializers import RegisterDndUser
from users.models import DndUser

# Create your views here.

class UserRegisterView(APIView):

    def get(self, request):
        return Response('test')
    
    def post(self, request):
        register_data = {
            'username': request.data.get('login'),
            'name': request.data.get('userName'),
            'password': request.data.get('userPassword'),
            'email': request.data.get('email'),
        }

        serializer = RegisterDndUser(data=register_data)
        if serializer.is_valid():
            register_user = DndUser.objects.create(
                username = register_data['username'],
                name = register_data['name'],
                email = register_data['email'],
                is_staff = False,
            )
            register_user.set_password(register_data['password'])
            register_user.save()

            send_mail(
                'Register data dnd', 
                f'Hello your register data is Login{register_user.email} Password {register_data["password"]}', 
                'demonvans@yandex.ru', [f'{register_data["email"]}'], fail_silently=False
            )

            return Response('user_created', status=status.HTTP_201_CREATED)
        
        return Response('error 404', status=status.HTTP_404_NOT_FOUND)
    
class UserRecoverPasswordView(APIView):

    def post(self, request):
        recover_email = request.data.get('email')
        target_user = get_object_or_404(DndUser, email=recover_email)
        print(request.data.get('email'))
        if target_user:
            password = generate_user_password()
            target_user.set_password(password)
            target_user.save()
            send_mail(
                'Register data dnd', 
                f'Hello your register data is Login{target_user.email} Password {password}', 
                'demonvans@yandex.ru', [f'{target_user.email}'], fail_silently=False
            )

            return Response('password send to email', status=status.HTTP_200_OK)
        
        return Response('not found', status=status.HTTP_404_NOT_FOUND)

    
class UserLoginView(APIView):
    
    def post(self, request):
        target_user_email = request.data.get('email')
        target_user_password = request.data.get('password')
        target_user = get_object_or_404(DndUser, email=target_user_email)
        target_user.check_password(request.data['password'])
        if not target_user.check_password(request.data['password']):
            return Response('login failed', status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=target_user)

        authenticate(email = target_user.email, password = target_user.password)

        user = {
            "userId": target_user.id,
            "login":target_user.username,
            "userName": target_user.name, 
            "userEmail":target_user.email,
            'token': token.key,
            'isAdmin': target_user.is_staff,
            'auth': True, 
        }

        return Response(user, status=status.HTTP_200_OK)
    
class UserLogoutView(APIView):

    def post(self, request):
        target_user_email = request.data.get('email')
        target_user_id = request.data.get('id')
        target_user = get_object_or_404(DndUser, id =  target_user_id,  email=target_user_email)
        user_token = get_object_or_404(Token, user=target_user)

        logout(request)
        Token.objects.get(user=target_user_id).delete()

        return Response('logout success', status=status.HTTP_200_OK)
            

def generate_user_password():
    password = secrets.token_urlsafe(6)
    return password