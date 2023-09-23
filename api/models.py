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
    class_abilities = models.ManyToManyField('ReferenceBookAbilityItem', through='ReferenceBookClassAbility', null=True, blank=True)
    class_mastery = models.ManyToManyField('WeaponMasteryItem', through='WeaponCharMastery', null=True, blank=True)
    class_armor_mastery = models.ManyToManyField('ArmorMasteryItem', through='ArmorCharMastery', null=True, blank=True)

    book_id = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, related_name='charclass')

    class Meta:
        verbose_name = 'char_class'
        verbose_name_plural = 'char_classes'

    def __str__(self):

        return self.char_classname
    
class ReferenceBookCharSubClass(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=3000, blank=True)

    main_class = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='subclass')

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
    
    mastery_book_id = models.ForeignKey(ReferenceBookMastery, on_delete=models.CASCADE, related_name='mastery_skill')

class WeaponCharMastery(models.Model):
    all_simple_weapons = models.BooleanField(null=True, blank=True, default=False)
    all_warriors_weapons = models.BooleanField(null=True, blank=True, default=False)
    all_exotic_weapons = models.BooleanField(null=True, blank=True, default=False)
    class_id = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='weapon_mastery')
    mastery_id = models.ForeignKey(WeaponMasteryItem, on_delete=models.CASCADE, related_name='char_weapon_mastery')

class ArmorMasteryItem(models.Model):
    name = models.TextField(max_length=255, unique=True)

    mastery_book_id = models.ForeignKey(ReferenceBookMastery, on_delete=models.CASCADE, related_name='armor_mastery')

class ArmorCharMastery(models.Model):
    mastery_id = models.ForeignKey(ArmorMasteryItem, on_delete=models.CASCADE, related_name='char_armor_mastery')
    class_id = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='char_armor_mastery')

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

class ReferenceBookSkills(models.Model):
    book_name = models.CharField(max_length=255)
    book_id = models.OneToOneField(ReferenceBook, on_delete=models.CASCADE, related_name='race_skills')

class ReferenceBookSubraceItemSkill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    skill_book = models.ForeignKey(ReferenceBookSkills, on_delete=models.CASCADE, related_name='subrace_skill')

class ReferenceBookItemSkillSubrace(models.Model):
    subrace_id = models.ForeignKey(ReferenceBookSubRace, on_delete=models.CASCADE, related_name='subrace_skills')
    skill_id = models.ForeignKey(ReferenceBookSubraceItemSkill, on_delete=models.CASCADE, related_name='subrace_skills')

class ReferenceBookItemSkill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    skill_book = models.ForeignKey(ReferenceBookSkills, on_delete=models.CASCADE, related_name='race_skill')

class ReferenceBookItemSkillRace(models.Model):
    race_id = models.ForeignKey(ReferenceBookCharRace, on_delete=models.CASCADE, related_name='race_skills')
    skill_id = models.ForeignKey(ReferenceBookItemSkill, on_delete=models.CASCADE, related_name='race_skills')

class ReferenceBookAbilityItem(models.Model):
    name = models.CharField(max_length=255)
    skill_book = models.ForeignKey(ReferenceBookSkills, on_delete=models.CASCADE, related_name='abilities')

class ReferenceBookClassAbility(models.Model):
    class_id = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='class_ability')
    ablility_id = models.ForeignKey(ReferenceBookAbilityItem, on_delete=models.CASCADE, related_name='ability')


class ReferenceBookLanguges(models.Model):
    book_name = models.CharField(max_length=255)
    book_id = models.OneToOneField(ReferenceBook, on_delete=models.CASCADE, related_name='book_languges')

class ReferenceBookLangugeItem(models.Model):
    name = models.CharField(max_length=255)
    lang_book = models.ForeignKey(ReferenceBookLanguges, on_delete=models.CASCADE, related_name='lang_item')

class ReferenceBookLangugeItemRace(models.Model):
    race_id = models.ForeignKey(ReferenceBookCharRace, on_delete=models.CASCADE, related_name='race_languges')
    languge_id = models.ForeignKey(ReferenceBookLangugeItem, on_delete=models.CASCADE, related_name='race_languges')

class InstrumentsMenu(models.Model):
    menu_name = models.CharField(max_length=255, unique=True)

class InstrumentItem(models.Model):
    name = models.CharField(max_length=255, unique=True)

    menu_id = models.ForeignKey(InstrumentsMenu, on_delete=models.CASCADE, related_name='instrument')
