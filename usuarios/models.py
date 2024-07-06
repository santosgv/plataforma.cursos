from django.db import models
from django.contrib.auth.models import AbstractUser

class USUARIO(AbstractUser):
    cpf = models.CharField(blank=True, max_length=18)
    is_gestor = models.BooleanField(default=False)
    alunos = models.ManyToManyField('self', related_name='gestores', symmetrical=False, blank=True)