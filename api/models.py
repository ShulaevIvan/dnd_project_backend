from django.db import models


class ReferenceBook(models.Model):
    book_name = models.CharField(max_length=255, default='reference_book')

    class Meta:
        verbose_name = 'reference_book'
        verbose_name_plural = 'reference_books'

    def __str__(self):

        return self.book_name
    
class ReferenceBookMenu(models.Model):
    menu_item_name = models.CharField(max_length=255)
    
    book_id = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, related_name='ref_menu')
    

class ReferenceBookCharClass(models.Model):
    char_classname = models.CharField(max_length=255, unique=True)
    base_hits = models.IntegerField()
    min_hits_lvl = models.IntegerField()
    max_hits_lvl = models.IntegerField()
    hits_by_lvl = models.IntegerField(null=True, blank=True)
    subclass_avalible = models.BooleanField()
    description = models.TextField(max_length=3000, blank=True, null=True)
    ability_count = models.IntegerField(null=True, blank=True)
    spellcaster = models.BooleanField(null=True, blank=True)
    spellcaster_main_stat = models.CharField(max_length=3, blank=True, null=True)
    # spell_сells = models.ManyToManyField('SpellCell', through='ClassSpellCell')
    class_abilities = models.ManyToManyField('ReferenceBookAbilityItem', through='ReferenceBookClassAbility')
    class_skills = models.ManyToManyField('ReferenceBookItemClassSkill', through='ReferenceBookClassSkill')
    class_main_stats = models.ManyToManyField('ClassMainAttrItem', through='ClassMainAttr')
    class_mastery = models.ManyToManyField('WeaponMasteryItem', through='WeaponCharMastery')
    class_armor_mastery = models.ManyToManyField('ArmorMasteryItem', through='ArmorCharMastery')
    class_instrument_mastery = models.ManyToManyField('InstrumentMasteryItem', through='InstrumentClassMastery')

    book_id = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, related_name='charclass')

    class Meta:
        verbose_name = 'char_class'
        verbose_name_plural = 'char_classes'

    def __str__(self):

        return self.char_classname
    
class ReferenceBookCharSubClass(models.Model):

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=3000, blank=True)
    spellcaster = models.BooleanField(null=True, blank=True)
    subclass_main_stats = models.ManyToManyField('ClassMainAttrItem', through='SubclassMainAttr')
    subclass_skills = models.ManyToManyField('ReferenceBookItemClassSkill', through='ReferenceBookSubClassSkill')

    main_class = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='subclass')

class MainSpellbook(models.Model):
    name = models.CharField(max_length=255)

    book_id = models.OneToOneField(ReferenceBook, on_delete=models.CASCADE, related_name='main_spellbook')

class ClassSpellbook(models.Model):
    name = models.CharField(max_length=255)
    spells = models.ManyToManyField('SpellItem', through='ClassSpellItem')
    class_id = models.OneToOneField(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='class_spellbook')

class SpellItem(models.Model):
    name = models.CharField(max_length=255)
    spell_level = models.IntegerField(null=True)
    spell_type = models.CharField(max_length=255)
    school = models.CharField(max_length=255, null=True, blank=True)
    action_cost = models.IntegerField()
    bonuce_action = models.BooleanField()
    duratation = models.IntegerField(null=True,)
    duratation_value = models.CharField(max_length=255)
    spell_target = models.CharField(max_length=255)
    distance = models.IntegerField(null=True,)
    concentration = models.BooleanField()
    description = models.TextField(max_length=3000)

    spellbook_id = models.ForeignKey(MainSpellbook, on_delete=models.CASCADE, related_name='spell_item')

class ClassSpellItem(models.Model):

    spellbook_id = models.ForeignKey(ClassSpellbook, on_delete=models.CASCADE, related_name='class_spellbook')
    spell_id = models.ForeignKey(SpellItem, on_delete=models.CASCADE, related_name='class_spell')

class CellPattern(models.Model):
    level_required = models.IntegerField()
    modifer = models.IntegerField()
    max_spells = models.IntegerField(null=True, blank=True)
    sorcery_points = models.IntegerField(null=True, blank=True)
    spell_invocation = models.IntegerField(null=True, blank=True)
    max_special_spells = models.IntegerField(null=True, blank=True)
    level_0_cells_qnt = models.IntegerField(null=True, blank=True)
    level_1_cells_qnt = models.IntegerField(null=True, blank=True)
    level_2_cells_qnt = models.IntegerField(null=True, blank=True)
    level_3_cells_qnt = models.IntegerField(null=True, blank=True)
    level_4_cells_qnt = models.IntegerField(null=True, blank=True)
    level_5_cells_qnt = models.IntegerField(null=True, blank=True)
    level_6_cells_qnt = models.IntegerField(null=True, blank=True)
    level_7_cells_qnt = models.IntegerField(null=True, blank=True)
    level_8_cells_qnt = models.IntegerField(null=True, blank=True)
    level_9_cells_qnt = models.IntegerField(null=True, blank=True)

    class_id = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='cells_pattern')


class ReferenceBookMastery(models.Model):
    name = models.CharField(max_length=255)

    book_id = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, related_name='mastery_book')

class SaveThrowItem(models.Model):
    name = models.CharField(max_length=255)

    mastery_book_id = models.ForeignKey(ReferenceBookMastery, on_delete=models.CASCADE, related_name='save_throw')

class ClassSaveThrow(models.Model):

    save_throw_id = models.ForeignKey(SaveThrowItem, on_delete=models.CASCADE, related_name='save_throw_item')
    class_id = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='class_save_throw')
    
class WeaponMasteryItem(models.Model):
    name = models.TextField(max_length=255, unique=True)
    range_weapon = models.BooleanField()
    melee_weapon = models.BooleanField()
    warrior_weapon = models.BooleanField()
    exotic_weapon = models.BooleanField()
    simple_weapon = models.BooleanField()
    fundamental_skill = models.BooleanField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    mastery_type = models.CharField(max_length=255, null=True, blank=True)

    mastery_book_id = models.ForeignKey(ReferenceBookMastery, on_delete=models.CASCADE, related_name='mastery_skill')

class WeaponCharMastery(models.Model):
    all_simple_weapons = models.BooleanField(null=True, blank=True, default=False)
    all_warriors_weapons = models.BooleanField(null=True, blank=True, default=False)
    all_exotic_weapons = models.BooleanField(null=True, blank=True, default=False)

    class_id = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='weapon_mastery')
    mastery_id = models.ForeignKey(WeaponMasteryItem, on_delete=models.CASCADE, related_name='char_weapon_mastery')

class ArmorMasteryItem(models.Model):
    name = models.TextField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    fundamental_skill = models.BooleanField(null=True, blank=True)
    mastery_type = models.CharField(max_length=255, null=True, blank=True)

    mastery_book_id = models.ForeignKey(ReferenceBookMastery, on_delete=models.CASCADE, related_name='armor_mastery')

class ArmorCharMastery(models.Model):
    mastery_id = models.ForeignKey(ArmorMasteryItem, on_delete=models.CASCADE, related_name='char_armor_mastery')
    class_id = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='char_armor_mastery')

class InstrumentMasteryItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)
    fundamental_skill = models.BooleanField(null=True, blank=True)
    mastery_type = models.CharField(max_length=255, null=True, blank=True)

    mastery_book_id = models.ForeignKey(ReferenceBookMastery, on_delete=models.CASCADE, related_name='instrument_mastery')

class InstrumentClassMastery(models.Model):

    mastery_id = models.ForeignKey(InstrumentMasteryItem, on_delete=models.CASCADE, related_name='char_instrument_mastery')
    class_id = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='char_instrument_mastery')

class ReferenceBookCharRace(models.Model):
    char_race_name = models.CharField(max_length=255, unique=True)
    subrace_avalible = models.BooleanField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    race_description = models.TextField(max_length=3000)
    preferred_worldview = models.CharField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField('ReferenceBookItemSkill', through='ReferenceBookItemSkillRace')
    languges = models.ManyToManyField('ReferenceBookLangugeItem', through='ReferenceBookLangugeItemRace')

    book_id = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, related_name='char_race')

class ReferenceBookSubRace(models.Model):
    subrace_name = models.CharField(max_length=255)
    subrace_active = models.BooleanField()
    race_description = models.TextField(max_length=3000, blank=True, null=True)
    skills = models.ManyToManyField('ReferenceBookSubraceItemSkill',  through='ReferenceBookItemSkillSubrace')
    race_id = models.ForeignKey(ReferenceBookCharRace, on_delete=models.CASCADE, related_name='subrace', blank=True, null=True)

class ReferenceBookSubRaceBonuces(models.Model):
    str_bonuce = models.IntegerField(null=True, blank=True)
    dex_bonuce = models.IntegerField(null=True, blank=True)
    con_bonuce = models.IntegerField(null=True, blank=True)
    int_bonuce = models.IntegerField(null=True, blank=True)
    wis_bonuce = models.IntegerField(null=True, blank=True)
    cha_bonuce = models.IntegerField(null=True, blank=True)

    subrace_id = models.OneToOneField(ReferenceBookSubRace, on_delete=models.CASCADE, related_name='subrace_bonuce', blank=True)

class ReferenceBookCharRaceBonuces(models.Model):
    str_bonuce = models.IntegerField(null=False)
    dex_bonuce = models.IntegerField(null=False)
    con_bonuce = models.IntegerField(null=False)
    int_bonuce = models.IntegerField(null=False)
    wis_bonuce = models.IntegerField(null=False)
    cha_bonuce = models.IntegerField(null=False)
    
    race_id = models.OneToOneField(ReferenceBookCharRace, on_delete = models.CASCADE, related_name='race_bonuces', primary_key = True)

class ReferenceBookClassSkills(models.Model):
    book_name = models.CharField(max_length=255)
    book_id = models.OneToOneField(ReferenceBook, on_delete=models.CASCADE, related_name='class_skills')

class ReferenceBookItemClassSkill(models.Model):
    name = models.CharField(max_length=255)
    level_required = models.IntegerField()
    skill_description = models.TextField(max_length=3000, null=True, blank=True)

    book_id = models.ForeignKey(ReferenceBookClassSkills, on_delete=models.CASCADE, related_name='class_skill')
    
class ReferenceBookClassSkill(models.Model):

    skill_id = models.ForeignKey(ReferenceBookItemClassSkill, on_delete=models.CASCADE, related_name='char_class_skills')
    class_id = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='char_class_skills')

class ReferenceBookSubClassSkill(models.Model):

    skill_id = models.ForeignKey(ReferenceBookItemClassSkill, on_delete=models.CASCADE, related_name='char_subclass_skills')
    subclass_id = models.ForeignKey(ReferenceBookCharSubClass, on_delete=models.CASCADE, related_name='char_subclass_skills')

class ReferenceBookSkills(models.Model):
    book_name = models.CharField(max_length=255)
    book_id = models.OneToOneField(ReferenceBook, on_delete=models.CASCADE, related_name='race_skills')

class ReferenceBookSubraceItemSkill(models.Model):
    name = models.CharField(max_length=255)
    skill_description = models.TextField()
    skill_type = models.CharField(max_length=100)
    skill_value = models.IntegerField(blank=True, null=True)
    skill_book = models.ForeignKey(ReferenceBookSkills, on_delete=models.CASCADE, related_name='subrace_skill')

class ReferenceBookItemSkillSubrace(models.Model):
    subrace_id = models.ForeignKey(ReferenceBookSubRace, on_delete=models.CASCADE, related_name='subrace_skills')
    skill_id = models.ForeignKey(ReferenceBookSubraceItemSkill, on_delete=models.CASCADE, related_name='subrace_skills')

class ReferenceBookItemSkill(models.Model):
    name = models.CharField(max_length=255)
    skill_description = models.TextField()
    skill_type = models.CharField(max_length=100)
    skill_data = models.CharField(null=True, blank=True)
    skill_value = models.IntegerField(blank=True, null=True)
    skill_book = models.ForeignKey(ReferenceBookSkills, on_delete=models.CASCADE, related_name='race_skill')

class ReferenceBookItemSkillRace(models.Model):
    race_id = models.ForeignKey(ReferenceBookCharRace, on_delete=models.CASCADE, related_name='race_skills')
    skill_id = models.ForeignKey(ReferenceBookItemSkill, on_delete=models.CASCADE, related_name='race_skills')

class ReferenceBookAbilityItem(models.Model):
    name = models.CharField(max_length=255)
    ability_description = models.TextField(blank=True)
    ability_type = models.CharField(max_length=5)
    skill_book = models.ForeignKey(ReferenceBookSkills, on_delete=models.CASCADE, related_name='abilities')

class ReferenceBookClassAbility(models.Model):
    class_id = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='class_ability')
    ablility_id = models.ForeignKey(ReferenceBookAbilityItem, on_delete=models.CASCADE, related_name='ability')

class ItemsEquipBook(models.Model):
    name = models.CharField(max_length=255)

    book_id = models.OneToOneField(ReferenceBook, on_delete=models.CASCADE, related_name='items_eqip_book')

class WeaponItemEquip(models.Model):
    name = models.CharField(max_length=255, unique=True)
    min_dmg = models.IntegerField()
    max_dmg = models.IntegerField()
    dmg_type = models.CharField(max_length=255)
    effective_range = models.IntegerField()
    max_range = models.IntegerField()
    ranged_weapon = models.BooleanField()
    melee_weapon = models.BooleanField()
    onehanded = models.BooleanField()
    twohanded = models.BooleanField()
    weight = models.IntegerField()
    default_price = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    item_type = models.CharField(max_length=255, blank=True, null=True)

    book_id = models.ForeignKey(ItemsEquipBook, on_delete=models.CASCADE, related_name='item_weapons')

class ArmorItemEquip(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    default_price = models.IntegerField(null=True, blank=True)
    base_armor = models.IntegerField()
    dex_modif = models.IntegerField()
    dex_modif_full = models.BooleanField()
    sneak_penalty = models.BooleanField(blank=True)
    light_armor = models.BooleanField(blank=True)
    medium_armor = models.BooleanField(blank=True)
    heavy_armor = models.BooleanField(blank=True)
    shield = models.BooleanField(blank=True)
    weight = models.IntegerField()
    item_type = models.CharField(max_length=255, blank=True, null=True)

    book_id = models.ForeignKey(ItemsEquipBook, on_delete=models.CASCADE, related_name='item_armor')

class InstrumentItemEquip(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    default_price = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField()
    item_type = models.CharField(max_length=255, blank=True, null=True)

    book_id = models.ForeignKey(ItemsEquipBook, on_delete=models.CASCADE, related_name='item_instruments')

class OtherItemEquip(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    default_price = models.IntegerField(null=True, blank=True)
    item_type = models.CharField(max_length=255, blank=True, null=True)

    book_id = models.ForeignKey(ItemsEquipBook, on_delete=models.CASCADE, related_name='item_other')

class ItemEqipTemplate(models.Model):

    template_name = models.CharField(max_length=255)

    start_weapons = models.ManyToManyField(WeaponItemEquip, through='CharClassStartEqipWeapon')
    start_armor = models.ManyToManyField(ArmorItemEquip, through='CharClassStartEqipArmor')
    start_instruments = models.ManyToManyField(InstrumentItemEquip, through='CharClassStartEqipInsrument')

    char_class = models.OneToOneField(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='start_items_template')
    
class CharClassStartEqipWeapon(models.Model):

    quantity = models.IntegerField(default=1)

    start_weapon_id = models.ForeignKey(WeaponItemEquip, on_delete=models.CASCADE, related_name='start_weapon_eqip')
    template_id = models.ForeignKey(ItemEqipTemplate, on_delete=models.CASCADE, related_name='item_eqip_weapons')

class CharClassStartEqipArmor(models.Model):

    quantity = models.IntegerField(default=1)

    start_armor_id = models.ForeignKey(ArmorItemEquip, on_delete=models.CASCADE, related_name='start_armor_eqip')
    template_id = models.ForeignKey(ItemEqipTemplate, on_delete=models.CASCADE, related_name='item_eqip_armor')

class CharClassStartEqipInsrument(models.Model):

    quantity = models.IntegerField(default=1)

    start_instruments = models.ForeignKey(InstrumentItemEquip, on_delete=models.CASCADE, related_name='start_other_eqip')
    template_id = models.ForeignKey(ItemEqipTemplate, on_delete=models.CASCADE, related_name='item_eqip_instruments')

class CharClassStartEqipOther(models.Model):

    quantity = models.IntegerField(default=1)

    start_other = models.ForeignKey(OtherItemEquip, on_delete=models.CASCADE, related_name='start_other_eqip')
    template_id = models.ForeignKey(ItemEqipTemplate, on_delete=models.CASCADE, related_name='item_eqip_other')

class ReferenceBookLanguges(models.Model):
    book_name = models.CharField(max_length=255)

    book_id = models.OneToOneField(ReferenceBook, on_delete=models.CASCADE, related_name='book_languges')

class ReferenceBookLangugeItem(models.Model):
    name = models.CharField(max_length=255)

    lang_book = models.ForeignKey(ReferenceBookLanguges, on_delete=models.CASCADE, related_name='lang_item')

class ReferenceBookLangugeItemRace(models.Model):
    race_id = models.ForeignKey(ReferenceBookCharRace, on_delete=models.CASCADE, related_name='race_languges')
    languge_id = models.ForeignKey(ReferenceBookLangugeItem, on_delete=models.CASCADE, related_name='race_languges')

class ReferenceBookBackground(models.Model):
    name = models.CharField(max_length=255)

    book_id = models.OneToOneField(ReferenceBook, on_delete=models.CASCADE, related_name='background')

class BackgroundItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)
    non_combat_items_eqip = models.TextField(max_length=3000)
    weapon_mastery = models.ManyToManyField('WeaponMasteryItem', through='BackgroundWeaponSkill')
    armor_mastery = models.ManyToManyField('ArmorMasteryItem', through='BackgroundArmorSkill')
    instrument_mastery = models.ManyToManyField('InstrumentMasteryItem', through='BackgroundInstrumentSkill')
    
    background_skills = models.ManyToManyField('BackgroundSkillItem', through='BackgroundSkill')
    abilities = models.ManyToManyField('ReferenceBookAbilityItem', through='BackgroundAbility')
    languages = models.ManyToManyField('ReferenceBookLangugeItem', through='BackgroundLanguge')
    weapons = models.ManyToManyField('WeaponItemEquip', through='BackgroundWeaponEqip')
    armor = models.ManyToManyField('ArmorItemEquip', through='BackgroundArmorEqip')
    instruments = models.ManyToManyField('InstrumentItemEquip', through='BackgroundInstrumentEqip')

    book_id = models.ForeignKey(ReferenceBookBackground, on_delete=models.CASCADE, related_name='background_item')


class BackgroundLanguge(models.Model):
    language_id = models.ForeignKey(ReferenceBookLangugeItem, on_delete=models.CASCADE, related_name='background_language')
    background_id = models.ForeignKey(BackgroundItem, on_delete=models.CASCADE, related_name='background_language')

class BackgroundAbility(models.Model):

    ability_id = models.ForeignKey(ReferenceBookAbilityItem, on_delete=models.CASCADE, related_name='background_ability')
    background_id = models.ForeignKey(BackgroundItem, on_delete=models.CASCADE, related_name='background_ability')

class BackgroundSkillItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)


class BackgroundSkill(models.Model):

    background_id = models.ForeignKey(BackgroundItem, on_delete=models.CASCADE, related_name='background_skill')
    skill_id = models.ForeignKey(BackgroundSkillItem, on_delete=models.CASCADE, related_name='background_skill')

class BackgroundWeaponSkill(models.Model):

    weapon_mastery_id = models.ForeignKey(WeaponMasteryItem, on_delete=models.CASCADE, related_name='background_weapon_mastery')
    background_id = models.ForeignKey(BackgroundItem, on_delete=models.CASCADE, related_name='background_weapon_skill')

class BackgroundArmorSkill(models.Model):

    armor_mastery_id = models.ForeignKey(ArmorMasteryItem, on_delete=models.CASCADE, related_name='background_armor_mastery')
    background_id = models.ForeignKey(BackgroundItem, on_delete=models.CASCADE, related_name='background_armor_skill')

class BackgroundInstrumentSkill(models.Model):

    instrument_mastery_id = models.ForeignKey(InstrumentMasteryItem, on_delete=models.CASCADE, related_name='background_instrument_mastery')
    background_id = models.ForeignKey(BackgroundItem, on_delete=models.CASCADE, related_name='background_instrument_skill')

class BackgroundWeaponEqip(models.Model):

    weapon_id = models.ForeignKey(WeaponItemEquip, on_delete=models.CASCADE, related_name='background_weapon_eqip')
    background_id = models.ForeignKey(BackgroundItem, on_delete=models.CASCADE, related_name='background_weapon')

class BackgroundArmorEqip(models.Model):

    armor_id = models.ForeignKey(ArmorItemEquip, on_delete=models.CASCADE, related_name='background_armor_eqip')
    background_id = models.ForeignKey(BackgroundItem, on_delete=models.CASCADE, related_name='background_armor')

class BackgroundInstrumentEqip(models.Model):

    instrument_id = models.ForeignKey(InstrumentItemEquip, on_delete=models.CASCADE, related_name='background_instrument_eqip')
    background_id = models.ForeignKey(BackgroundItem, on_delete=models.CASCADE, related_name='background_instrument')

class BackgroundAttrs(models.Model):

    str_attr = models.IntegerField()
    dex_attr = models.IntegerField()
    con_attr = models.IntegerField()
    int_attr = models.IntegerField()
    wis_attr = models.IntegerField()
    cha_attr = models.IntegerField()

    background_id = models.OneToOneField(BackgroundItem, on_delete=models.CASCADE, related_name='background_attrs')


class ClassAttrsBook(models.Model):

    book_id = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, related_name='class_attrs_book')


class ClassMainAttrItem(models.Model):

    name = models.CharField(max_length=255, unique=True)

    book_id = models.ForeignKey(ClassAttrsBook, on_delete=models.CASCADE, related_name='class_attr_item')

class ClassMainAttr(models.Model):

    class_attr_id = models.ForeignKey(ClassMainAttrItem, on_delete=models.CASCADE, related_name='class_attr_item')
    class_id = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='class_attr')

class SubclassMainAttr(models.Model):

    subclass_attr_id = models.ForeignKey(ClassMainAttrItem, on_delete=models.CASCADE, related_name='subclass_attr_item')
    subclass_id = models.ForeignKey(ReferenceBookCharSubClass, on_delete=models.CASCADE, related_name='subclass_attr')



class InstrumentsMenu(models.Model):
    menu_name = models.CharField(max_length=255, unique=True)

class InstrumentItem(models.Model):
    name = models.CharField(max_length=255, unique=True)

    menu_id = models.ForeignKey(InstrumentsMenu, on_delete=models.CASCADE, related_name='instrument')


class CharacterName(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(null=True, blank=True)