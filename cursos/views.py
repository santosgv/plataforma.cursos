
import json
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Comentarios, Cursos,Aulas, NotasAulas


def home(request):
    if request.user.is_authenticated:
        cursos = Cursos.objects.all().order_by('nome')
        return render(request, 'home.html', {'cursos': cursos, 'request_usuario': request.user})
    else:
        return render(request, 'home.html')

def curso(request, id):
    if request.user.is_authenticated:
        aulas = Aulas.objects.filter(curso = id)
        return render(request, 'curso.html', {'aulas': aulas, 'request_usuario': request.user})
    else:
        return redirect('/auth/login/?status=2')

def aula(request, id):
    if request.user.is_authenticated:
        aula = Aulas.objects.get(id = id)
        comentarios = Comentarios.objects.filter(aula = aula).order_by('-data')
        usuario_avaliou = NotasAulas.objects.filter(aula_id = id).filter(usuario_id = request.user.id)
        avaliacoes = NotasAulas.objects.filter(aula_id = id)



        return render(request, 'aula.html', {'aula': aula,
                                            'usuario_id': request.user.id,
                                            'comentarios': comentarios,
                                            'request_usuario': request.user,
                                            'usuario_avaliou': usuario_avaliou,
                                            'avaliacoes': avaliacoes})
    else:
        return redirect('/auth/login/?status=2')

def comentarios(request):
    #usuario_id = int(request.user.id)
    comentario = request.POST.get('comentario')
    aula_id = int(request.POST.get('aula_id'))

    comentario_instancia = Comentarios(usuario_id = request.user.id,
                                       comentario = comentario,
                                       aula_id = aula_id)
    comentario_instancia.save()
    comentarios = Comentarios.objects.filter(aula = aula_id).order_by('-data')
    somente_nomes = [i.usuario.first_name for i in comentarios]
    somente_comentarios = [i.comentario for i in comentarios]
    comentarios = list(zip(somente_nomes, somente_comentarios))

    return HttpResponse(json.dumps({'status': '1', 'comentarios': comentarios }))

def processa_avaliacao(request):
    if request.user.is_authenticated:

        avaliacao = request.POST.get('avaliacao')
        aula_id = request.POST.get('aula_id')
        

        usuario_avaliou = NotasAulas.objects.filter(aula_id = aula_id).filter(usuario_id = request.user.id)


        if not usuario_avaliou:
            nota_aulas = NotasAulas(aula_id = aula_id,
                                    nota = avaliacao,
                                    usuario_id = request.user.id,
                                    )
            nota_aulas.save()
            return redirect(f'/home/aula/{aula_id}')
        else:
            return redirect(f'/home/aula/{aula_id}')

    else:
        return redirect('/auth/login/')