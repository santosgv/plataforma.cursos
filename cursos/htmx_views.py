
from .models import Comentarios
from django.shortcuts import render


def comentar(request,aula_id):
    comentario = request.POST.get('comentario')
    aula = int(request.POST.get('aula_id'))


    comentario_instancia = Comentarios(usuario_id = request.user.id,
                                       comentario = comentario,
                                       aula_id = aula)
    comentario_instancia.save()

    comentarios = Comentarios.objects.filter(aula = aula_id).order_by('-data')
    return render(request,'parcial/comentarios_parcial.html',{'comentarios':comentarios})


