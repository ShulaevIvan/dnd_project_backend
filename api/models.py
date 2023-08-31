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

    book_id = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, related_name='charclass')

    class Meta:
        verbose_name = 'char_class'
        verbose_name_plural = 'char_classes'

    def __str__(self):

        return self.char_classname
    
class ReferenceBookCharSubClass(models.Model):
    char_subclass = models.CharField(max_length=255, unique=True)

    main_class = models.ForeignKey(ReferenceBookCharClass, on_delete=models.CASCADE, related_name='subclass')


class ReferenceBookCharRace(models.Model):
    char_race_name = models.CharField(max_length=255, unique=True)
    subrace_avalible = models.BooleanField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    race_description = models.TextField(max_length=3000)
    languges = models.ManyToManyField('ReferenceBookLangugeItem', through='ReferenceBookLangugeItemRace')

    book_id = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, related_name='char_race')


class ReferenceBookSubRace(models.Model):
    subrace_name = models.CharField(max_length=255)
    subrace_active = models.BooleanField()
    race_description = models.TextField(max_length=3000, blank=True, null=True)
    race_id = models.ForeignKey(ReferenceBookCharRace, on_delete=models.CASCADE, related_name='subrace', blank=True, null=True)

class ReferenceBookSubRaceBonuces(models.Model):
    str_bonuce = models.IntegerField(null=True, blank=True)
    dex_bonuce = models.IntegerField(null=True, blank=True)
    con_bonuce = models.IntegerField(null=True, blank=True)
    int_bonuce = models.IntegerField(null=True, blank=True)
    wis_bonuce = models.IntegerField(null=True, blank=True)
    cha_bonuce = models.IntegerField(null=True, blank=True)

    subrace_id = models.ForeignKey(ReferenceBookSubRace, on_delete=models.CASCADE, related_name='subrace_bonuces', blank=True)

class ReferenceBookSubRaceSkill(models.Model):
    skill_name = models.CharField(max_length=255)
    skill_description = models.TextField(max_length=5000)
    
    subrace_bonuce = models.ManyToManyField(ReferenceBookSubRaceBonuces, related_name='subrace_bonuce_skill', through='ReferenceBookSubRaceBonuceSkill', blank=True)

class ReferenceBookSubRaceBonuceSkill(models.Model): 
    skill_id = models.ForeignKey(ReferenceBookSubRaceSkill, on_delete=models.CASCADE, related_name='bonuce_skill', blank=True)
    subrace_bonuce_id  = models.ForeignKey(ReferenceBookSubRaceBonuces, on_delete=models.CASCADE, related_name='race_skill', blank=True)


class ReferenceBookCharRaceBonuces(models.Model):
    str_bonuce = models.IntegerField(null=False)
    dex_bonuce = models.IntegerField(null=False)
    con_bonuce = models.IntegerField(null=False)
    int_bonuce = models.IntegerField(null=False)
    wis_bonuce = models.IntegerField(null=False)
    cha_bonuce = models.IntegerField(null=False)

    race_id = models.OneToOneField(ReferenceBookCharRace, on_delete = models.CASCADE, related_name='race_bonuces', primary_key = True)

class ReferenceBookCharRaceSkill(models.Model):
    skill_name = models.CharField(max_length=255)
    skill_description = models.TextField(max_length=5000)
    race_bonuce = models.ManyToManyField(ReferenceBookCharRaceBonuces, related_name='race_bonuce_skill', through='ReferenceBookCharRaceBonuceSkill')

class ReferenceBookCharRaceBonuceSkill(models.Model):
    skill_id = models.ForeignKey(ReferenceBookCharRaceSkill, on_delete=models.CASCADE, related_name='bonuce_skill')
    race_bonuce_id  = models.ForeignKey(ReferenceBookCharRaceBonuces, on_delete=models.CASCADE, related_name='race_skill')

# class ReferenceBookLanguage(models.Model):
#     name = models.CharField(max_length=255)
#     book_id = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, related_name='race_languages')
#     race_id = models.ForeignKey(ReferenceBookCharRace, on_delete=models.CASCADE, related_name='languages', null=True, blank=True)


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
