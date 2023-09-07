from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.models import DndUser

class RegisterDndUser(ModelSerializer):

    class Meta(object):
        model = DndUser
        fields = ['username', 'password', 'email',]

class DetailRaceViewSerializer(serializers.Serializer):

    char_race_name = serializers.CharField(max_length=255,)
    subrace_avalible = serializers.BooleanField()
    age = serializers.IntegerField()
    speed = serializers.IntegerField()
    size = serializers.IntegerField()
    weight = serializers.CharField()
    race_description = serializers.CharField()
    book_id = serializers.IntegerField()

    def char_race_name(self, value):
        print(value)

