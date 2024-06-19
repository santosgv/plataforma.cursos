
from django.contrib import admin
from .models import Cursos, Aulas, Comentarios, NotasAulas,ProgressoAula

admin.site.register(Aulas)
admin.site.register(Cursos)
admin.site.register(Comentarios)
admin.site.register(NotasAulas)
admin.site.register(ProgressoAula)