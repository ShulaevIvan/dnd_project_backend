from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import WeaponItemEquipSerializer, ArmorItemEquipSerializer, InstrumentItemEquipSerializer
from .models import ReferenceBook, ReferenceBookCharClass, ReferenceBookMenu, InstrumentsMenu, CharacterName
from .models import ReferenceBookCharRace, ReferenceBookBackground, ReferenceBookSkills, ReferenceBookMastery, ClassSpellbook, ReferenceBookClassSkills

from itertools import chain
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import secrets
import random
import re
import random

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
    
class ReferenceBookSkillsView(APIView):
    
    def get(self, request):
        target_skill = request.GET.get('skill')
        result_data = []
        data = {
            'race_skills': get_object_or_404(ReferenceBookSkills, id=1).race_skill.all().values(),
            'subrace_skills': get_object_or_404(ReferenceBookSkills, id=1).subrace_skill.all().values(),
            'class_skills': get_object_or_404(ReferenceBookClassSkills, id=1).class_skill.all().values(),
        }
        if target_skill:
            for skill_arr in data.values():
                if len(skill_arr) > 0:
                    result_data.append([skill for skill in skill_arr if skill['name'].lower() == target_skill.lower()])
            
            return Response(*filter(lambda arr: arr, result_data), status=status.HTTP_200_OK)

        return Response(data, status=status.HTTP_200_OK)
    
class ReferenceBookAbilitesView(APIView):

    def get(self, request):
        ability = request.GET.get('ability')

        if ability:
            if not ability[0].isupper():
                ability = f'{ability[0].upper()}{ability[1:len(ability)]}'

            query = get_object_or_404(ReferenceBookSkills, id=1).abilities.filter(name=ability)
            ability = [{
                "id": abil['id'],
                "name": abil['name'],
                "abilityType": abil['ability_type'],
                "description": abil['ability_description'],
            }  for abil in query.values()]

            return Response(ability, status=status.HTTP_200_OK)

        if not ability:
            query = get_object_or_404(ReferenceBookSkills, id=1).abilities.all()

            abilites = [{
                "id": abil['id'],
                "name": abil['name'],
                "abilityType": abil['ability_type'],
                "description": abil['ability_description'],
            }  for abil in query.values()]

            return Response(abilites, status=status.HTTP_200_OK)
    
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

        return Response(weapons, status=status.HTTP_200_OK)

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

        return Response(all_mastery, status=status.HTTP_200_OK)

class ReferenceBookItemsView(APIView):

    def get(self, request):
        params = request.query_params
        items = {}
        query_book = get_object_or_404(ReferenceBook, id=1)

        if params.get('chunk') and params.get('chunk').isdigit():
            max_items = int(params.get('chunk'))

            chunks = [random.randint(1, round(max_items / 3)) for i in range(3)]
            chunks_sum = sum(chunks)
            if chunks_sum < max_items:
                dif = max_items - chunks_sum
                chunks[random.randint(0, len(chunks) - 1)] += dif

            weapon_objects_count = query_book.items_eqip_book.item_weapons.count()
            armor_objects_count = query_book.items_eqip_book.item_armor.count()
            instruments_objects_count = query_book.items_eqip_book.item_instruments.count()

            weapon_serializer = WeaponItemEquipSerializer(data=query_book.items_eqip_book.item_weapons.all().values(), many=True)
            armor_serizlizer = ArmorItemEquipSerializer(data=query_book.items_eqip_book.item_armor.all().values(), many=True)
            instrument_serializer = InstrumentItemEquipSerializer(data=query_book.items_eqip_book.item_instruments.all().values(), many=True)

            weapon_serializer.is_valid()
            armor_serizlizer.is_valid()
            instrument_serializer.is_valid()

            rand_weapons = [weapon_serializer.data[random.randint(0, weapon_objects_count - 1)] for i in range(chunks[0])]
            rand_armor = [armor_serizlizer.data[random.randint(0, armor_objects_count - 1)] for i in range(chunks[1])]
            rand_instruments = [ instrument_serializer.data[random.randint(0, instruments_objects_count - 1)] for i in range(chunks[2])]

            items = {
                'weapons': rand_weapons,
                'armor': rand_armor,
                'instruments': rand_instruments
            }

            return Response({'items': items}, status=status.HTTP_200_OK)
        
        if params.get('item'):
            item_name = f"{params.get('item')[0].upper()}{params.get('item')[1:len(params.get('item'))]}"
            weapon_serializer = WeaponItemEquipSerializer(
                data=list(query_book.items_eqip_book.item_weapons.filter(name=item_name).all().values()), many=True
            )
            armor_serizlizer = ArmorItemEquipSerializer(
                data=list(query_book.items_eqip_book.item_armor.filter(name=item_name).all().values()), many=True
            )
            instrument_serializer = InstrumentItemEquipSerializer(
                data=list(query_book.items_eqip_book.item_instruments.filter(name=item_name).all().values()), many=True
            )
            weapon_serializer.is_valid()
            armor_serizlizer.is_valid()
            instrument_serializer.is_valid()
           
            target_item = {
                'weapon': weapon_serializer.data,
                'armor': armor_serizlizer.data,
                'instruments': instrument_serializer.data
            }
            target_item = [arr for key, arr in target_item.items() if len(arr) > 0]

            return Response({'items': target_item}, status=status.HTTP_200_OK)
                    
        if params.get('filter') == 'weapons':
            weapons = WeaponItemEquipSerializer(data=query_book.items_eqip_book.item_weapons.all().values(), many=True)
            weapons.is_valid()

            return Response({'weapons': weapons.data}, status=status.HTTP_200_OK) 
        
        elif params.get('filter') == 'armor':
            armor = ArmorItemEquipSerializer(data=query_book.items_eqip_book.item_armor.all().values(), many=True)
            armor.is_valid()

            return Response({'armor': armor.data}, status=status.HTTP_200_OK)
        
        elif params.get('filter') == 'instruments':
            instruments = InstrumentItemEquipSerializer(data=query_book.items_eqip_book.item_instruments.all().values(), many=True)
            instruments.is_valid()

            return Response({'instruments': instruments.data}, status=status.HTTP_200_OK)
        
        weapons = WeaponItemEquipSerializer(data=query_book.items_eqip_book.item_weapons.all().values(), many=True)
        armor = ArmorItemEquipSerializer(data=query_book.items_eqip_book.item_armor.all().values(), many=True)
        instruments = InstrumentItemEquipSerializer(data=query_book.items_eqip_book.item_instruments.all().values(), many=True)

        weapons.is_valid()
        armor.is_valid()
        instruments.is_valid()

        items = {
            'weapons':weapons.data,
            'armor': armor.data,
            'instruments': instruments.data,
        }
        
        return Response({'items': items}, status=status.HTTP_200_OK)
    
    def post(self, request):
        request_data = json.loads(request.body)
        add_items_count = request_data.get('count')
        existing_items_ids = request_data.get('existingItems')
        if not existing_items_ids and not add_items_count: return Response({'status': 'err'})
        existing_weapons = list(filter(lambda item: item['type'] == 'weapon', request_data.get('existingItems')))
        existing_armor = list(filter(lambda item: item['type'] == 'armor', request_data.get('existingItems')))
        existing_instruments = list(filter(lambda item: item['type'] == 'instrument', request_data.get('existingItems')))

        excludeing_ids = []
        for weapon in existing_weapons:
            excludeing_ids.append(weapon['id'])
        
        query_book = get_object_or_404(ReferenceBook, id=1)

        weapons =  WeaponItemEquipSerializer(data=query_book.items_eqip_book.item_weapons.all().exclude(id__in=[1,3,4]).values(), many=True)
        weapons.is_valid()

        return Response({'status': weapons.data})

class ReferenceBookLanguagesView(APIView):

    def get(self, request):
        
        query = get_object_or_404(ReferenceBook, id=1)
        languges = [{'id': lang_obj.id, 'name': lang_obj.name} for lang_obj in query.book_languges.lang_item.all().exclude(id=9)]

        return Response(languges, status=status.HTTP_200_OK)

class InstrumentsView(APIView):
    
    def get(self, request):
        query = get_object_or_404(InstrumentsMenu, id=1).instrument.all().values()
        clear_data = [{'id': inst['id'], 'name': inst['name']} for inst in query]

        return Response({'instruments': clear_data})


class RandomCharacterNameView(APIView):

    def get(self, request, gender):
        number = request.GET.get('num')
        data = {}
        random_names = []
        
        if gender != 'all' and gender != 'male' and 'gender'and gender != 'female':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if number and int(number):
            if gender == 'all':
                names_list = list(CharacterName.objects.all())
            else:
                names_list = list(CharacterName.objects.all().filter(gender=gender))

            for i in range(int(number)):
                random_names.append(
                    {
                        'name': names_list[random.randint(0, len(names_list))].name, 
                        'gender': names_list[random.randint(0, len(names_list))].gender
                    }
                )
        else:
            if gender == 'all':
                query = CharacterName.objects.all().order_by('?').first()
            else:
                query = CharacterName.objects.filter(gender=gender).order_by('?').first()
            random_names.append({'name': query.name, gender: query.gender})
 
        return Response(random_names, status=status.HTTP_200_OK)
        
def generate_user_password():
    password = secrets.token_urlsafe(6)

    return password
