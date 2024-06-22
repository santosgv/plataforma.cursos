
from django.contrib import admin
from .models import Cursos, Aulas, Comentarios, NotasAulas,ProgressoAula

admin.site.register(Aulas)
admin.site.register(Cursos)
admin.site.register(Comentarios)
admin.site.register(NotasAulas)

@admin.register(ProgressoAula)
class ProgressoAdmin(admin.ModelAdmin):
    list_display = ('usuario','baixou_certificado',)
    list_filter = ('usuario','baixou_certificado',)
    readonly_fields=('baixou_certificado','concluida','aula','usuario')
    

