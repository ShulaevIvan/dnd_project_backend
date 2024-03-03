from django.shortcuts import render

from users.models import DndUser, UserCharacter, UserCharacterStat, UserCharacterAbility, UserCharacterSubclass, \
UserCharacterSavethrow, UserCharacterLanguage, UserCharacterArmorMastery, UserCharacterWeaponMastery, \
UserCharacterInstrumentMastery, UserCharacterSkill, UserCharacterSpell, UserCharacterInventory, UserCharacterInventroryMoney, CharacterInventoryItem, \
UserCharacterInventoryItem, UserCharacterInventroryMoney

from api.models import SpellItem, ItemsEquipBook

from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from pprint import pprint
import re
import os
import base64
import uuid
import datetime
import json
from .serializers import UserCharacterSpellSerializer

class UserCharacterView(APIView):

    def get(self, request, user_id):
        query = get_object_or_404(DndUser, id=user_id)
        
        if query.email:

            user_characters = [
                {
                    'id': character['id'],
                    'creationTime': character['character_created_time'],
                    'modifedTime': character['character_modifed_time'],
                    'name': character['character_name'],
                    'description': character['character_description'],
                    'avatar': character['character_avatar_id'],
                    'lvl': character['character_level'],
                    'race': character['character_race'],
                    'class': character['character_class'],
                    'background': character['character_background'],
                    'baseArmor': character['character_base_armor'],
                    'hitDice': character['character_hit_dice'],
                    'maxHits': character['character_max_hits'],
                    'initiative': character['character_initiative'],
                    'moveSpeed': character['character_speed'],
                    'passivePresep': character['character_passive_preseption'],
                    'worldview': character['character_worldview'],
                    'charSize': character['character_size'],
                    'charWeight': character['character_weight'],

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
                    'spells': [
                        {
                            'spell_id': spell['spell_id']
                        } for spell in UserCharacter.objects.get(id=character['id']).char_spells.all().values()
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
                    'armorMastery': [
                        {
                            'name': armor_mastery['name']
                        } 
                        for armor_mastery in UserCharacter.objects.get(id=character['id']).char_armor_mastery.all().values()
                    ],
                    'weaponMastery': [
                        {
                            'name': weapon_mastery['name']
                        } 
                        for weapon_mastery in UserCharacter.objects.get(id=character['id']).char_weapon_mastery.all().values()
                    ],
                    'instrumentMastery': [
                        {
                            'name': instrument_mastery['name']
                        } 
                        for instrument_mastery in UserCharacter.objects.get(id=character['id']).char_instrument_mastery.all().values()
                    ],
                    'inventory': {
                        'inventoryItems': [
                            {
                                'item': CharacterInventoryItem.objects.filter(id=inventory_item['id']).values(),
                                'quantity': inventory_item['quantity']
                            }
                            for inventory_item in UserCharacterInventory.objects.get(character_id=character['id']).character_inventory_item.all().values()
                        ],
                        'inventoryGold': {
                            'gold': UserCharacterInventory.objects.get(character_id=character['id']).money.gold,
                            'silver': UserCharacterInventory.objects.get(character_id=character['id']).money.silver,
                            'bronze': UserCharacterInventory.objects.get(character_id=character['id']).money.bronze
                        }
                    }
                   
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
            'character_spells': request.data.get('charSpells'),
            'character_inventory': request.data.get('charInventory'),
        }
        character_exists = UserCharacter.objects.filter(
            dnd_user_id = user_id, 
            character_name = character_data['character_name'],
            character_level = character_data['character_level']
        )

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

        inventory, created_inventory = UserCharacterInventory.objects.get_or_create(character_id=created_character)
        
        if character_data['character_inventory'].get('weapons'):
            for weapon_obj in character_data['character_inventory']['weapons']:
                item, created_item = CharacterInventoryItem.objects.get_or_create(name=weapon_obj['name'], item_type='weapon')
                UserCharacterInventoryItem.objects.update_or_create(item_id=item, character_id=inventory, quantity=1)
                
            for armor_obj in character_data['character_inventory']['armor']:
                item, created_item = CharacterInventoryItem.objects.get_or_create(name=armor_obj['name'], item_type='armor')
                UserCharacterInventoryItem.objects.update_or_create(item_id=item, character_id=inventory, quantity=1)

            for instrument_obj in character_data['character_inventory']['instruments']:
                item, created_item = CharacterInventoryItem.objects.get_or_create(name=instrument_obj['name'], item_type='instrument')
                UserCharacterInventoryItem.objects.update_or_create(item_id=item, character_id=inventory, quantity=1)


        
        if character_data['character_inventory'].get('currency'):
            UserCharacterInventroryMoney.objects.update_or_create(
                gold=character_data['character_inventory']['currency']['money']['gold'],
                silver=character_data['character_inventory']['currency']['money']['silver'],
                bronze=character_data['character_inventory']['currency']['money']['bronze'],
                inventory_id=inventory
            )
        
        if character_exists:
            UserCharacter.objects.filter(
                dnd_user_id = created_character.dnd_user_id,
                character_name = created_character.character_name,
                character_level = created_character.character_level,
            ).update(
                character_modifed_time=datetime.datetime.now()
            )
        
        if character_data['character_spells']:
            for spell in character_data['character_spells']:
                UserCharacterSpell.objects.update_or_create(character_id=created_character, spell_id=spell['id'])

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
                file.write(base64.b64decode(character_data['character_avatar']['data']))

        return Response(request.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, user_id):
        target_character_id = request.data.get('characterId')
        target_character_name = request.data.get('characterName')
        
        target_character = get_object_or_404(UserCharacter, id=target_character_id, character_name=target_character_name)
        target_character.delete().save()


        return Response({'status': 'ok'}, status=status.HTTP_204_NO_CONTENT)
    

class UserCharacterControl(APIView):

    def get(self, request, user_id, character_id):
        params = request.query_params
        avatar_id = request.GET.get('avatar')

        if avatar_id:
            query = get_object_or_404(UserCharacter, character_avatar_id=avatar_id)

            return Response({
                'file_name': query.character_avatar_name,
                'file_data': query.character_avatar_data, 
                'file_ext': query.character_avatar_ext,
                'file_type': 'test',
            })

        if not params:
            query_user_character = UserCharacter.objects.filter(dnd_user=user_id, id=character_id)
            if not query_user_character.exists():
                return Response({'status': 'not found'}, status=status.HTTP_404_NOT_FOUND)
            
            view_data = [
                {
                    'id': character_obj['id'],
                    'avatar': character_obj['character_avatar_id'],
                    'name': character_obj['character_name'],
                    'description': character_obj['character_description'],
                    'level': character_obj['character_level'],
                    'race': character_obj['character_race'],
                    'class': character_obj['character_class'],
                    'subclass': character_obj['character_subclass'],
                    'background': character_obj['character_background'],
                    'worldview': character_obj['character_worldview'],
                    'weight': character_obj['character_weight'],
                    'weight': character_obj['character_weight'],
                    'age': character_obj['character_age'],
                    'weight': character_obj['character_weight'],
                    'size': character_obj['character_size'],
                    'stats': [{
                        'name': stat['name'],
                        'value': stat['value'],
                        'modifer': stat['modifer'],
                    } for stat in UserCharacter.objects.get(id=character_obj['id']).char_stats.all().values()],
                    'savethrows': [
                        {
                            'name': savethrow['name'],
                        } for savethrow in UserCharacter.objects.get(id=character_obj['id']).char_savethrows.all().values()
                    ],
                    'languages': [
                        {
                            'id': lang['id'], 
                            'name': lang['name'],
                        } 
                        for lang in UserCharacter.objects.get(id=character_obj['id']).char_languages.all().values()
                    ],
                    'hitDice': character_obj['character_hit_dice'],
                    'maxHits': character_obj['character_max_hits'],
                    'armor': character_obj['character_base_armor'],
                    'initiative': character_obj['character_initiative'],
                    'speed': character_obj['character_speed'],
                    'masteryPoints': character_obj['character_mastery'],
                    'passivePreseption': character_obj['character_passive_preseption'],
                    'abilities': [{
                        'name': ability['name'],
                        'value': ability['value'],
                        'type': ability['ability_type'],
                    } for ability in UserCharacter.objects.get(id=character_obj['id']).char_abilities.all().values()],
                    'spells': [{
                        'id': spell['id'],
                        'spell_id': SpellItem.objects.get(id=spell['id']).id,
                        'name': SpellItem.objects.get(id=spell['id']).name,
                        'name': SpellItem.objects.get(id=spell['id']).description,

                    } for spell in UserCharacter.objects.get(id=character_id).char_spells.all().values()],
                    'inventory': {
                        'inventoryItems': [
                            {
                                'item': CharacterInventoryItem.objects.filter(id=inventory_item['id']).values(),
                                'quantity': inventory_item['quantity']
                            }
                            for inventory_item in UserCharacterInventory.objects.get(character_id=character_obj['id']).character_inventory_item.all().values()
                        ],
                        'inventoryGold': {
                            'gold': UserCharacterInventory.objects.get(character_id=character_obj['id']).money.gold,
                            'silver': UserCharacterInventory.objects.get(character_id=character_obj['id']).money.silver,
                            'bronze': UserCharacterInventory.objects.get(character_id=character_obj['id']).money.bronze
                        }
                    },
                    'created': character_obj['character_created_time'],
                    'mofied': character_obj['character_modifed_time'],
                } for character_obj in query_user_character.values()
            ][0]
            return Response({'character': view_data}, status=status.HTTP_200_OK)
        

        return Response({
            'status': 'not found'
        }, status=status.HTTP_200_OK)
    
class UserCharacterSpellsView(APIView):

    class Meta:
        serializer_class = UserCharacterSpellSerializer

    def get(self, request, user_id, character_id):
        all_params = request.query_params
        
        if all_params.get('spell') == 'all':
            query_spells = get_object_or_404(UserCharacter, id=character_id, dnd_user_id=user_id).char_spells.all().values('spell_id')
            spell_data = [UserCharacterSpellSerializer(SpellItem.objects.filter(id=spell_obj['spell_id']), many=True).data[0] for spell_obj in query_spells]
            
            return Response({'spells': spell_data}, status=status.HTTP_200_OK)

      
class UserCharacterInventoryView(APIView):

    def get(self, request, user_id, character_id):

        params = request.query_params
        images_folder = f'{os.getcwd()}/app_data/character_items/images/'
        item_filter = params.get('filter')
        item_name = params.get('item')
        inventory_data = {}

        all_items = {
            'weapons': ItemsEquipBook.objects.get(id=1).item_weapons.all().values(),
            'armor': ItemsEquipBook.objects.get(id=1).item_armor.all().values(),
            'instruments': ItemsEquipBook.objects.get(id=1).item_instruments.all().values(),
        }
        if not os.path.exists(images_folder):
            os.mkdir(f'{os.getcwd()}/app_data/character_items/')
            os.mkdir(f'{os.getcwd()}/app_data/character_items/images/')
            with open(f'{os.getcwd()}/app_data/character_items/images/test_img.jpg', 'w') as test_img:
                test_img.write('tset')
        
        if not params:
            inventory_data = {
                'items': [{
                    'id': item.id,
                    'name': item.name,
                    'type': item.item_type,
                    'itemId': get_item_id_by_item_type(item.name, item.item_type),
                    'quantity': item.character_inventory_item.filter(item_id=item.id, character_id=character_id).values_list('quantity', flat=True)[0],
                    'image': {
                        'data': get_base64(images_folder, 'item_img.jpg'),
                        'ext': 'image/jpeg'
                    }
                } for item in get_object_or_404(UserCharacter, id=character_id).char_inventory.items.all()],
            }

            for item_obj in inventory_data['items']:
                if item_obj['type'] == 'armor':
                    item_data = ItemsEquipBook.objects.get(id=1) \
                        .item_armor.filter(name=item_obj['name']).values_list(flat=True)
                elif item_obj['type'] == 'weapon':
                    item_data = ItemsEquipBook.objects.get(id=1) \
                        .item_weapons.filter(name=item_obj['name']).values_list(flat=True)
                elif item_obj['type'] == 'instrument':
                    item_data = ItemsEquipBook.objects.get(id=1) \
                        .item_instruments.filter(name=item_obj['name']).values_list(flat=True)
                
                if len(item_data) > 0:
                    item_obj['description'] = item_data.values_list('description', flat=True)[0]
                    item_obj['price'] = item_data.values_list('default_price', flat=True)[0]
                    if item_obj['type'] =='armor':
                        item_obj['stats'] = item_data.values('base_armor','dex_modif', 'dex_modif_full',
                            'sneak_penalty', 'light_armor', 'medium_armor', 'heavy_armor', 'shield','weight')[0]
                    elif item_obj['type'] =='weapon':
                        item_obj['stats'] = item_data.values('ranged_weapon', 'melee_weapon', 'onehanded', 
                            'twohanded', 'min_dmg', 'max_dmg','weight','effective_range', 'max_range', 'dmg_type',)[0]
                    elif item_obj['type'] == 'instrument':
                        item_obj['stats'] = item_data.values('weight')[0]

            return Response(inventory_data, status=status.HTTP_200_OK)
        
        check_char_item = get_object_or_404(UserCharacter, id=character_id).char_inventory.items.filter(name=item_name).exists()

        if item_filter:
            inventory_data = {
                'items': [item for item in UserCharacter.objects.get(id=character_id).char_inventory.items.filter(item_type=item_filter).values()],
            }
            return Response({'items': inventory_data}, status=status.HTTP_200_OK)
        
        if params.get('item') and check_char_item:
            character_inventory = get_object_or_404(UserCharacterInventory, character_id=character_id)
            items_qnt = [{
                'item_name': item_obj.name,
                'item_type': item_obj.item_type,
                'item_qnt': item_obj.character_inventory_item.filter(character_id=character_id).values_list('quantity', flat=True)[0]
            } for item_obj in character_inventory.items.all()]
            
            for key, arr in all_items.items():
                target_item = [item for item in arr if item['name'] == item_name]
                if target_item:
                    target_item[0]['quantity'] = [item_q for item_q in items_qnt if item_q['item_name'] == item_name][0]['item_qnt']
                    return Response({'items': target_item}, status=status.HTTP_200_OK)
                
        elif params.get('item') and not check_char_item:
            return Response({'items': []}, status=status.HTTP_200_OK)
    
    def post(self, request, user_id, character_id):
        params = request.query_params

        if params.get('add') == 'item':
            item_data = json.loads(request.body)
            character_id = item_data.get('characterId')
            item_name = item_data.get('itemName')
            item_type = item_data.get('itemType')
            
            target_character = get_object_or_404(UserCharacter, dnd_user = user_id, id=character_id, character_name = item_data['characterName'])
            check_item = target_character.char_inventory.items.filter(name=item_name, item_type=item_type)
            target_item_obj = CharacterInventoryItem.objects.filter(name=item_name, item_type=item_type).first()

            if not check_item.exists():
                UserCharacterInventoryItem.objects.update_or_create(
                    quantity = int(item_data.get('quantity')),
                    item_id = CharacterInventoryItem.objects.create(name=item_name, item_type=item_type),
                    character_id = UserCharacterInventory.objects.get(character_id=character_id)
                )
               

                return Response({'status': 'create'}, status=status.HTTP_201_CREATED)
            elif check_item.exists() and target_item_obj:
                for item in target_character.char_inventory.items.all():
                    if item.name == item_name and item.item_type == item_type:
                        new_qnt = int(item.character_inventory_item.all().values_list('quantity', flat=True)[0]) + int(item_data.get('quantity'))

                        UserCharacterInventoryItem.objects.update(
                            quantity = new_qnt,
                            item_id = target_item_obj,
                            character_id = UserCharacterInventory.objects.get(character_id=character_id)
                        )
                        return Response({'status': 'update'}, status=status.HTTP_201_CREATED)

        return Response({'status': 'create'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, user_id, character_id):
        params = request.query_params
        item_data = json.loads(request.body)
        character_inventory = get_object_or_404(UserCharacterInventory, character_id=character_id)

        for char_item in character_inventory.items.all():
            item_qnt = char_item.character_inventory_item.all().values_list('quantity', flat=True)
            if char_item.name == item_data['name'] and char_item.item_type == item_data['type'] and item_qnt and int(item_qnt[0]) <= 1:
                char_item.delete()
                item_data['status'] = 'removed'

                return Response(item_data, status=status.HTTP_202_ACCEPTED)
            elif char_item.name == item_data['name'] and char_item.item_type == item_data['type'] and item_qnt and int(item_qnt[0]) > 1:
                for item_field in char_item.character_inventory_item.all():
                    item_field.quantity = int(item_field.quantity) - int(item_data['count'])
                    item_field.save()
                    item_data['count'] = item_field.quantity
                
                item_data['status'] = 'reduced'
                return Response(item_data, status=status.HTTP_202_ACCEPTED)

        return Response({'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)

def get_item_id_by_item_type(item_name, item_type):
    items_book = ItemsEquipBook.objects.get(id=1)
    item = 0
    if item_type == 'weapon':
        item = items_book.item_weapons.filter(name=item_name, item_type = item_type).values_list('id', flat=True)[0]
    elif item_type == 'armor':
        item = items_book.item_armor.filter(name=item_name, item_type = item_type).values_list('id', flat=True)[0]
    elif item_type == 'instrument':
        item = items_book.item_instruments.filter(name=item_name, item_type = item_type).values_list('id', flat=True)[0]
    
    return item   
    
def get_base64(folder_path, image_name):
    with open(f'{folder_path}{image_name}', 'rb') as file:
        encoded_string = base64.b64encode(file.read())
    return encoded_string