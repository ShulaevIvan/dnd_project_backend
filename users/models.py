from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class DndUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(('email adress'), unique=True)