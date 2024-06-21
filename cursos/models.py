from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Cursos(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()
    thumb = models.ImageField(upload_to = "thumb_cursos")
    ativo= models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.nome
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

class Aulas(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()
    aula = models.FileField(upload_to = "aulas")
    curso = models.ForeignKey(Cursos, on_delete = models.DO_NOTHING)
    data_upload = models.DateField(default=now)
    ativo= models.BooleanField(default=True)
    

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'


    def __str__(self) -> str:
        return self.nome

class Comentarios(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    comentario = models.TextField()
    data = models.DateTimeField(default = datetime.now)
    aula = models.ForeignKey(Aulas, on_delete = models.DO_NOTHING)
    
    def __str__(self) -> str:
        return str(self.usuario)
    
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

class NotasAulas(models.Model):
    choices = (
        ('p', 'Péssimo'),
        ('r', 'Ruim'),
        ('re', 'Regular'),
        ('b', 'bom'),
        ('o', 'Ótimo')
    )

    aula = models.ForeignKey(Aulas, on_delete=models.DO_NOTHING)
    nota = models.CharField(max_length=50, choices=choices)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return str(self.usuario)
    
    class Meta:
        verbose_name = 'Avaliacao'
        verbose_name_plural = 'Avaliaçoes'

class ProgressoAula(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aulas, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.aula.nome}"

    class Meta:
        unique_together = ('usuario', 'aula')
        verbose_name = 'Progresso da Aula'
        verbose_name_plural = 'Progresso das Aulas'