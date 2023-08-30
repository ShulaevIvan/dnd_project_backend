from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import ReferenceBook, ReferenceBookCharClass, ReferenceBookMenu, InstrumentsMenu
from .models import ReferenceBookCharRace
from .serializers import DetailRaceViewSerializer
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

class ReferenceBookView(APIView):

    def get(self, request):
        book_menu = ReferenceBookMenu.objects.all()
        character_classes = ReferenceBook.objects.get(id=1).charclass.all()

        response_data = {
            'menu': [{'id': item['id'], 'name': item['menu_item_name'] }for item in book_menu.values()],
            'classes': [{'id': c['id'], 'classname': c['char_classname'] } for c in character_classes.values()]
        }

        return Response(response_data)


class ReferenceBookClassView(APIView):

    def get(self, request):
        char_class_req = request.GET.get('class', None)
        if not char_class_req:
            queryset = ReferenceBookCharClass.objects.all()
            clear_data = [{'id': c.id, 'classname': c.char_classname, 'allsubclass': c.subclass.all().values()} for c in queryset]
        else :
            char_class_req = char_class_req.lower()
            queryset = ReferenceBookCharClass.objects.get(char_classname = char_class_req)  
            clear_data = {'id': queryset.id, 'classname': queryset.id, 'allsubclass': queryset.subclass.all().values()}

        return Response(clear_data)
    
class ReferenceBookRaceView(APIView):

    def get(self, request):
        book = get_object_or_404(ReferenceBook, id=1).char_race.all()
        clear_data = []

        for race_obj in book:
            subraces = []
            subrace_data = {}
            subrace_skills = []
            subrace_bonuces = {}

            if race_obj.subrace_avalible:
                for subrace_obj in race_obj.subrace.all():
                    if subrace_obj.race_id_id == race_obj.id and subrace_obj.subrace_active:
                        for subrace_bonuce in subrace_obj.subrace_bonuces.all().filter(subrace_id = subrace_obj.id, subrace_bonuce_skill__isnull=False):
                            subrace_bonuces['str'] = subrace_bonuce.str_bonuce
                            subrace_bonuces['dex'] = subrace_bonuce.dex_bonuce
                            subrace_bonuces['con'] = subrace_bonuce.con_bonuce
                            subrace_bonuces['int'] = subrace_bonuce.int_bonuce
                            subrace_bonuces['wis'] = subrace_bonuce.wis_bonuce
                            subrace_bonuces['cha'] = subrace_bonuce.cha_bonuce

                            subrace_data = {
                                'subrace_id': subrace_obj.id,
                                'subrace_name': subrace_obj.subrace_name,
                            }

                            subrace_skills = [
                                {
                                    'id': skill.id, 
                                    'name': skill.skill_name, 
                                    'description': skill.skill_description
                                } for skill in subrace_bonuce.subrace_bonuce_skill.all()
                            ]
                            
            
            subrace_avalible = [s.subrace_name for s in race_obj.subrace.all()]
 
            
            if race_obj.race_bonuces.race_bonuce_skill:
                race_skills = [
                    {
                        'id': skill['id'], 
                        'skillname': skill['skill_name'], 
                        'description': skill['skill_description']
                    } for skill in race_obj.race_bonuces.race_bonuce_skill.all().values()
                ]


            clear_data.append({
                'id': race_obj.id,
                'name': race_obj.char_race_name,
                'description': race_obj.race_description,
                'age': race_obj.age,
                'speed': race_obj.speed,
                'size': race_obj.size,
                'weight': race_obj.weight,
                'subraceAvalible': subrace_avalible,
                'skills': race_skills,

                'bonuces': {
                    'str': race_obj.race_bonuces.str_bonuce,
                    'dex': race_obj.race_bonuces.dex_bonuce,
                    'con': race_obj.race_bonuces.con_bonuce,
                    'int': race_obj.race_bonuces.int_bonuce,
                    'wis': race_obj.race_bonuces.wis_bonuce,
                    'cha': race_obj.race_bonuces.cha_bonuce,
                },
                'subrace_active': subrace_data,
                'subrace_skills': subrace_skills,
                'subrace_bonuces': subrace_bonuces
            })
      
        return Response({'races': clear_data})
    
class DetailRaceView(APIView):

    def get(self, request, race_id):
        query_race = ReferenceBookCharRace.objects.all().filter(id = race_id)


        return Response({'status': list(query_race.values())})

class InstrumentsView(APIView):
    
    def get(self, request):
        query = get_object_or_404(InstrumentsMenu, id=1).instrument.all().values()
        clear_data = [{'id': inst['id'], 'name': inst['name']} for inst in query]

        return Response({'instruments': clear_data})

def generate_user_password():
    password = secrets.token_urlsafe(6)
    return password