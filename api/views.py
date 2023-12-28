from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import ReferenceBook, ReferenceBookCharClass, ReferenceBookMenu, InstrumentsMenu
from .models import ReferenceBookCharRace, ReferenceBookBackground, ReferenceBookSkills, ReferenceBookMastery, ClassSpellbook

from itertools import chain
from rest_framework.response import Response
from rest_framework.views import APIView
import json
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
        print(register_data)

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

            # send_mail(
            #     'Register data dnd', 
            #     f'Hello your register data is Login{register_user.email} Password {register_data["password"]}', 
            #     'demonvans@yandex.ru', [f'{register_data["email"]}'], fail_silently=False
            # )

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
        query_class = ReferenceBookCharClass.objects.all()
        clear_data = []

        for class_obj in query_class:

            clear_class_data = {}
            clear_class_data['class_data'] = {
                'id': class_obj.id,
                'name': class_obj.char_classname,
                'baseHits': class_obj.base_hits,
                'minHitsLvl': class_obj.min_hits_lvl,
                'maxHitsLvl': class_obj.max_hits_lvl,
                'hitsByLvl': class_obj.hits_by_lvl,
                'spellcaster': class_obj.spellcaster,
                'subclassAvalible': class_obj.subclass_avalible,
                'classSaveThrows': [{'id': throw.save_throw_id.id, 'name': throw.save_throw_id.name} for throw in class_obj.class_save_throw.all()],
                'description': class_obj.description
            }
            
            if class_obj.subclass_avalible:
                clear_class_data['subclases'] = [
                    {
                        'id': subclass.id, 
                        'name': subclass.name, 
                        'mainClass': subclass.main_class.id
                    } for subclass in class_obj.subclass.all()
                ]

            clear_data.append(clear_class_data)

        return Response(clear_data)
    
class DetailClassView(APIView):

    def get(self, reuqest, class_id):
        subclass_req = reuqest.GET.get('subclass')
        spells_cells_req = reuqest.GET.get('lvl')
        query_class = get_object_or_404(ReferenceBookCharClass, id=class_id)
        print(spells_cells_req)

        clear_data = {
            'id': query_class.id,
            'className': query_class.char_classname,
            'baseHits': query_class.base_hits,
            'minHitsLvl': query_class.min_hits_lvl,
            'maxHitsLvl': query_class.max_hits_lvl,
            'hitsByLvl': query_class.hits_by_lvl,
            'spellcaster': query_class.spellcaster,
            'spellcasterMainStat': query_class.spellcaster_main_stat,
            'spellCells': [
                {
                    'id': cell_pattern.id,
                    'levelRequired': cell_pattern.level_required,
                    'modifer': cell_pattern.modifer,
                    'maxSpells': cell_pattern.max_spells,
                    'maxSpecialSpells': cell_pattern.max_special_spells,
                    'sorceryPoints': cell_pattern.sorcery_points,
                    'spellInvocation': cell_pattern.spell_invocation,
                    'cellsLevel0': cell_pattern.level_0_cells_qnt,
                    'cellsLevel1': cell_pattern.level_1_cells_qnt,
                    'cellsLevel2': cell_pattern.level_2_cells_qnt,
                    'cellsLevel3': cell_pattern.level_3_cells_qnt,
                    'cellsLevel4': cell_pattern.level_4_cells_qnt,
                    'cellsLevel5': cell_pattern.level_5_cells_qnt,
                    'cellsLevel6': cell_pattern.level_6_cells_qnt,
                    'cellsLevel7': cell_pattern.level_7_cells_qnt,
                    'cellsLevel8': cell_pattern.level_8_cells_qnt,
                    'cellsLevel9': cell_pattern.level_9_cells_qnt,
                } for cell_pattern in query_class.cells_pattern.all()],
            'classAbilityPoints': query_class.ability_count,
            'classMainStats': [{'id': main_stat.class_attr_id.id, 'name': main_stat.class_attr_id.name }for main_stat in query_class.class_attr.all()],
            'classAbilities': [{'id': ability.ablility_id.id, 'name': ability.ablility_id.name} for ability in query_class.class_ability.all()],
            'classSkills': [
                {
                    'id': class_skill.skill_id.id, 
                    'name': class_skill.skill_id.name,
                    'levelRequired': class_skill.skill_id.level_required,
                    'description': class_skill.skill_id.skill_description,
                } 
                for class_skill in query_class.char_class_skills.all()
            ],
            'classSpells': [
                {
                    'id': spell_obj.id, 
                    'name': spell_obj.name,
                    'spellLevel': spell_obj.spell_level,
                    'school': spell_obj.school,
                    'actionCost': spell_obj.action_cost,
                    'bonuceAction': spell_obj.bonuce_action,
                    'duratation': spell_obj. duratation,
                    'duratationValue': spell_obj.duratation_value,
                    'spellTarget': spell_obj.spell_target,
                    'spellDistance': spell_obj.distance,
                    'concentrationTime': spell_obj.concentration,
                    'description': spell_obj.description
                } 
                for spell_obj in query_class.class_spellbook.spells.all()
            ],
            'classSaveThrows': [{'id': throw.save_throw_id.id, 'name': throw.save_throw_id.name} for throw in query_class.class_save_throw.all()],
            'classWeaponMastery': [{'id': class_obj.mastery_id.id, 'name': class_obj.mastery_id.name} for class_obj in query_class.weapon_mastery.all()],
            'classArmorMastery': [{'id': class_obj.mastery_id.id, 'name': class_obj.mastery_id.name} for class_obj in query_class.char_armor_mastery.all()],
            'classInstrumentMastery': [{'id': class_obj.mastery_id.id, 'name': class_obj.mastery_id.name} for class_obj in query_class.char_instrument_mastery.all()],
            'startEqip': {
                'weapons': [weapon_obj for weapon_obj in query_class.start_items_template.start_weapons.all().values()],
                'armor': [armor_obj for armor_obj in query_class.start_items_template.start_armor.all().values()],
                'instruments': [instr_obj for instr_obj in query_class.start_items_template.start_instruments.all().values()]
            },
            'subclassAvalible': query_class.subclass_avalible,
            'description': query_class.description,
            'subclasses': [],
        }

        if subclass_req and query_class.subclass_avalible:
            subclassdata = dict()
            target_subclass = query_class.subclass.all().filter(id=int(subclass_req))[0]
            subclassdata['id'] = target_subclass.id
            subclassdata['name'] = target_subclass.name
            subclassdata['description'] = target_subclass.description
            subclassdata['subclassSkills'] = [
                {
                    'id': skill_obj.skill_id.id, 
                    'name': skill_obj.skill_id.name,
                    'levelRequired': skill_obj.skill_id.level_required,
                    'description': skill_obj.skill_id.skill_description,
                } for skill_obj in target_subclass.char_subclass_skills.all()
            ]

            subclassdata['mainClassId'] = query_class.id
            clear_data['description'] = target_subclass.description
            clear_data['subraceActive'] = True
            clear_data['subclassInfo'] = subclassdata
            clear_data['subclassInfo'] = subclassdata
            clear_data.pop('subclassAvalible', None)
            clear_data.pop('subclasses', None)
            clear_data.pop('description', None)

        elif query_class.subclass_avalible and not subclass_req:
            for subclass in query_class.subclass.all():
                subclassdata = {
                    'id': subclass.id,
                    'name': subclass.name,
                    'description': subclass.description,
                    'mainClassId': subclass.main_class.id,
                }

                clear_data['subclasses'].append(subclassdata)
        
        return Response(clear_data)
    
class ReferenceBookRaceView(APIView):

    def get(self, request):

        races_query = ReferenceBookCharRace.objects.all()
        clear_data = {
            "races": []
        }

        for race in races_query.all():
            race_obj = {
                "id": race.id,
                "name": race.char_race_name,
                "subrace_avalible": race.subrace_avalible,
                "age" : race.subrace_avalible,
                "max_age" : race.max_age,
                "speed" : race.speed,
                "size" : race.size,
                "weight" : race.weight,
                "race_description" : race.race_description,
                "preferred_worldview" : race.preferred_worldview,
            }

            if race.subrace_avalible:
                race_obj['subraces'] = list(race.subrace.all().filter(race_id = race.id).values())
           
           
            clear_data['races'].append(race_obj)

        return Response(clear_data)
    
class DetailRaceView(APIView):

    def get(self, request, race_id):
        target_subrace = request.GET.get('subrace')
        query_race = ReferenceBookCharRace.objects.all().filter(id = race_id)

        if not query_race.exists():
            return Response({'status': 'not found'})
        
        race_bonuces = {}
        subrace_active_all_data = {
            "subrace_bonuces": {}
        }
        langusges = []

        for race_param in query_race.all():
            if target_subrace:
                for subrace in race_param.subrace.all().filter(subrace_name = target_subrace):
                    subrace_active_all_data['subrace_id'] = subrace.id
                    if race_param.subrace_avalible and subrace.subrace_bonuce:
                        subrace_active_all_data['subrace_bonuces']['str_bonuce'] = subrace.subrace_bonuce.str_bonuce
                        subrace_active_all_data['subrace_bonuces']['dex_bonuce'] = subrace.subrace_bonuce.dex_bonuce
                        subrace_active_all_data['subrace_bonuces']['int_bonuce'] = subrace.subrace_bonuce.int_bonuce
                        subrace_active_all_data['subrace_bonuces']['con_bonuce'] = subrace.subrace_bonuce.con_bonuce
                        subrace_active_all_data['subrace_bonuces']['wis_bonuce'] = subrace.subrace_bonuce.wis_bonuce
                        subrace_active_all_data['subrace_bonuces']['cha_bonuce'] = subrace.subrace_bonuce.cha_bonuce

                   
                    subrace_active_all_data['subrace_active_name'] = subrace.subrace_name
                    subrace_active_all_data['skills'] = list(subrace.skills.all().values())

            else:
                for subrace in race_param.subrace.all():
                    if race_param.subrace_avalible and subrace.subrace_bonuce:
                        subrace_active_all_data['subrace_bonuces']['str_bonuce'] = subrace.subrace_bonuce.str_bonuce
                        subrace_active_all_data['subrace_bonuces']['dex_bonuce'] = subrace.subrace_bonuce.dex_bonuce
                        subrace_active_all_data['subrace_bonuces']['int_bonuce'] = subrace.subrace_bonuce.int_bonuce
                        subrace_active_all_data['subrace_bonuces']['con_bonuce'] = subrace.subrace_bonuce.con_bonuce
                        subrace_active_all_data['subrace_bonuces']['wis_bonuce'] = subrace.subrace_bonuce.wis_bonuce
                        subrace_active_all_data['subrace_bonuces']['cha_bonuce'] = subrace.subrace_bonuce.cha_bonuce

                    
                    subrace_active_all_data['subrace_active_name'] = subrace.subrace_name
                    subrace_active_all_data['skills'] = list(subrace.skills.all().values())
                
        
        for lang_obj in query_race.all():
            langusges = [lang for lang in lang_obj.languges.all().values()]
        
        for skill_obj in query_race.all():
            skills = [skill for skill in skill_obj.skills.all().values()]


        clear_data = {
            "data": list(query_race.values()),
            "skills": skills,
            "languages": langusges,
            "race_bonuce_data": race_bonuces,
            "subrace_bonuce_data": [subrace_active_all_data],
        }
        
        for race_obj in query_race:
            clear_data['race_bonuces'] = {
                    "str_bonuce": race_obj.race_bonuces.str_bonuce,
                    "dex_bonuce": race_obj.race_bonuces.dex_bonuce,
                    "con_bonuce": race_obj.race_bonuces.con_bonuce,
                    "int_bonuce": race_obj.race_bonuces.int_bonuce,
                    "wis_bonuce": race_obj.race_bonuces.wis_bonuce,
                    "cha_bonuce": race_obj.race_bonuces.cha_bonuce,
            }
        
        return Response(clear_data)
    
class CharacterBackgroundView(APIView):

    def get(self, request):
        query = get_object_or_404(ReferenceBook, id=1)
        clear_data = dict()

        clear_data = [
            {
                'id': background_obj.id, 
                'name': background_obj.name,
                'description': background_obj.description,
            } for background_obj in query.background.background_item.all()
        ]


        return Response(clear_data)

class DetailBackgroundView(APIView):

    def get(self, request, background_id):
        query = get_object_or_404(ReferenceBookBackground, id=1)
        clear_data = [
            {
                'id': background_obj.id,
                'name': background_obj.name,
                'description': background_obj.description,
                'items': background_obj.non_combat_items_eqip,
                'weaponMastery': background_obj.weapon_mastery.all().values(),
                'armorMastery': background_obj.armor_mastery.all().values(),
                'instrumentMastery': background_obj.instrument_mastery.all().values(),
                'weapons': background_obj.weapons.all().values(),
                'armor': background_obj.armor.all().values(),
                'instruments': background_obj.armor.all().values(),
                'bounceAbilities': background_obj.abilities.all().values(),
                'languages': background_obj.languages.all().values(),
                
            } for background_obj in query.background_item.all().filter(id=background_id)
        ]

        return Response(clear_data)
    
class ReferenceBookSpellsView(APIView):

    def get(self, request):
        spell_lvl = request.GET.get('level')
        char_class_id = request.GET.get('class')

        if spell_lvl:
            all_spells = get_object_or_404(ReferenceBook, id=1).main_spellbook.spell_item.filter(spell_level=spell_lvl)
        elif char_class_id and spell_lvl:
            all_spells = get_object_or_404(ClassSpellbook, id=char_class_id).spells.filter(spell_level=spell_lvl)
        elif char_class_id:
            all_spells = get_object_or_404(ClassSpellbook, id=char_class_id).spells.all()
        else:
            all_spells = get_object_or_404(ReferenceBook, id=1).main_spellbook.spell_item.all()

        return Response(all_spells.values())
    
class DetailSpellView(APIView):

    def get(self, request, spell_id):
        spell = get_object_or_404(ReferenceBook, id=1).main_spellbook.spell_item.filter(id=spell_id)
        
        return Response(spell.values())
    
class ReferenceBookAbilitesView(APIView):

    def get(self, request):
        query = get_object_or_404(ReferenceBookSkills, id=1).abilities.all()
        abilites = [{
            "id": abil['id'],
            "name": abil['name'],
            "abilityType": abil['ability_type'],
        }  for abil in query.values()]

        return Response(abilites)
    
class ReferenceBookInstrumentsSkillView(APIView):

    def get(self, request):
        query = get_object_or_404(ReferenceBookMastery, id=3)
        instruments = [{
            'id': instrument_obj.id, 
            'name': instrument_obj.name,
            'description': instrument_obj.description
        }for instrument_obj in query.instrument_mastery.all()]

        return Response(instruments)
    
class ReferenceBookArmorSkillView(APIView):

    def get(self, request):
        query = get_object_or_404(ReferenceBookMastery, id=2)
            
        armor = [{
            'id': armor_obj.id, 
            'name': armor_obj.name,
        } for armor_obj in query.armor_mastery.all()]

        return Response(armor)
    
class ReferenceBookWeaponSkillView(APIView):

    def get(self, request):
        query = get_object_or_404(ReferenceBookMastery, id=1)
        weapons = [{
            'id': weapon_obj.id, 
            'name': weapon_obj.name,
        }for weapon_obj in query.mastery_skill.all()]

        return Response(weapons)


class ReferenceBookMasteryView(APIView):
    
    def get(self, request):

        param = request.GET.get('mastery')
        fundamentals_param = request.GET.get('fundamental')

        if (fundamentals_param):
            fundamentals_param = True

        if param and param == 'armor':
            query = get_object_or_404(ReferenceBookMastery, id=2)
            
            armor = [{
                'id': armor_obj.id, 
                'name': armor_obj.name,
            } for armor_obj in query.armor_mastery.all()]


            return Response(armor)
        
        elif param and param == 'weapons':
            query = get_object_or_404(ReferenceBookMastery, id=1)
            weapons = [{
                'id': weapon_obj.id, 
                'name': weapon_obj.name,
            }for weapon_obj in query.mastery_skill.all()]

            return Response(weapons)
        
        elif param and param == 'instruments':
            query = get_object_or_404(ReferenceBookMastery, id=3)
            instrument = [{
                'id': instrument_obj.id, 
                'name': instrument_obj.name,
                'description': instrument_obj.description
            }for instrument_obj in query.instrument_mastery.all()]

            return Response(instrument)
        
        armor = get_object_or_404(ReferenceBookMastery,id=2)
        weapon = get_object_or_404(ReferenceBookMastery,id=1)
        instrument = get_object_or_404(ReferenceBookMastery,id=3)

        all_mastery = {
            'armor': armor.armor_mastery.all().values(),
            'weapons': weapon.mastery_skill.all().values(),
            'instruments': instrument.instrument_mastery.all().values(),
        }

        return Response(all_mastery)
    

    
class ReferenceBookLanguagesView(APIView):

    def get(self, request):
        
        query = get_object_or_404(ReferenceBook, id=1)
        languges = [{'id': lang_obj.id, 'name': lang_obj.name} for lang_obj in query.book_languges.lang_item.all().exclude(id=9)]

        return Response(languges)


class CalculateStatsView(APIView):

    def post(self, request):
        print(request)
        return Response({'status': 'ok'})


class InstrumentsView(APIView):
    
    def get(self, request):
        query = get_object_or_404(InstrumentsMenu, id=1).instrument.all().values()
        clear_data = [{'id': inst['id'], 'name': inst['name']} for inst in query]

        return Response({'instruments': clear_data})

def generate_user_password():
    password = secrets.token_urlsafe(6)

    return password

