from django.db import models
from django.contrib.auth.models import AbstractUser

class USUARIO(AbstractUser):
    cpf = models.CharField(blank=True, max_length=18)