from rest_framework.serializers import ModelSerializer
from users.models import DndUser

class RegisterDndUser(ModelSerializer):

    class Meta(object):
        model = DndUser
        fields = ['username', 'password', 'email',]