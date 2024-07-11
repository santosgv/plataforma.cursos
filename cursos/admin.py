
from django.contrib import admin
from .models import Cursos, Aulas, Comentarios, NotasAulas,ProgressoAula,Contato

admin.site.register(Aulas)
admin.site.register(Cursos)
admin.site.register(Comentarios)
admin.site.register(NotasAulas)

@admin.register(ProgressoAula)
class ProgressoAdmin(admin.ModelAdmin):
    list_display = ('usuario','baixou_certificado',)
    list_filter = ('usuario','baixou_certificado',)
    readonly_fields=('baixou_certificado','concluida','aula','usuario')
    
@admin.action(description="Marcar como Lido")
def action_read_messenger(modeladmin,request,queryset):
    for mensagem in queryset:
        mensagem.Lido = True
        mensagem.save()

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('Nome','Email','assunto','Mensagem','Lido')
    readonly_fields=('Nome','Email','assunto','Mensagem')
    list_filter = ('Lido',)
    actions = [action_read_messenger,]