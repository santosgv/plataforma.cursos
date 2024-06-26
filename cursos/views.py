
import json
import io
import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,landscape
from django.http import HttpResponse,FileResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render,redirect
from .models import Comentarios, Cursos,Aulas, NotasAulas, ProgressoAula
from django.db import transaction
from .utils import marcar_aula_concluida, calcular_progresso_curso, pode_emitir_certificado
from django.core.paginator import Paginator


@login_required
def verificar_progresso(request, curso_id):
    curso = get_object_or_404(Cursos, id=curso_id)
    progresso = calcular_progresso_curso(request.user, curso_id)
    certificado_disponivel = pode_emitir_certificado(request.user, curso_id)
    return render(request, 'progresso.html', {'curso': curso, 'progresso': progresso, 'certificado_disponivel': certificado_disponivel})

@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def cursos(request):
    paginas_cursos=Cursos.objects.all().filter(ativo=True).order_by('nome')
    pagina = Paginator(paginas_cursos, 25)
    page = request.GET.get('page')
    cursos = pagina.get_page(page)
    return render(request, 'cursos.html', {'cursos': cursos,})

@login_required
def curso(request, id):
    paginas_aulas = Aulas.objects.filter(curso = id).filter(ativo=True).order_by('nome')
    pagina = Paginator(paginas_aulas, 25)
    page = request.GET.get('page')
    aulas = pagina.get_page(page)
    return render(request, 'curso.html', {'aulas': aulas,})

@login_required
def aula(request, id):

    aula = Aulas.objects.get(id = id)
    comentarios = Comentarios.objects.filter(aula = aula).order_by('-data')
    usuario_avaliou = NotasAulas.objects.filter(aula_id = id).filter(usuario_id = request.user.id)
    avaliacoes = NotasAulas.objects.filter(aula_id = id)

    
    marcar_aula_concluida(request.user, aula.id)
    return render(request, 'aula.html', {'aula': aula,
                                        'usuario_id': request.user.id,
                                        'comentarios': comentarios,
                                        'request_usuario': request.user,
                                        'usuario_avaliou': usuario_avaliou,
                                        'avaliacoes': avaliacoes})

@login_required
def comentarios(request):
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

@transaction.atomic
@login_required
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
    

@transaction.atomic
@login_required
def baixar_certificado(request,curso_id):
    progresso = ProgressoAula.objects.get(usuario=request.user,aula__curso=curso_id)
    curso = Cursos.objects.get(id=curso_id)
    progresso.baixou_certificado = True
    progresso.save()
    try:
        buffer = io.BytesIO()
        PDF = canvas.Canvas(buffer, pagesize=landscape(letter))
        PDF.setFont('Times-Roman', 30)
        image_path = os.path.join(settings.BASE_DIR, 'templates', 'certificado.jpeg')
        PDF.drawImage(image_path, 0, 0, width=landscape(letter)[0], height=landscape(letter)[1])
        PDF.drawString(230,390,str(request.user.first_name))
        PDF.setFont('Times-Roman', 20)
        PDF.drawString(395,359,str(request.user.cpf))
        PDF.setFont('Times-Roman', 15)

        if curso.cargoraria and curso.validade == 1:
            PDF.drawString(305,328,str(curso.nome + f',com Cargo Horária {curso.cargoraria} Hora Validade:{curso.validade} Ano'))
        else:
            PDF.drawString(305,328,str(curso.nome + f',com Cargo Horária {curso.cargoraria} Horas Validade:{curso.validade} Anos'))

        PDF.drawString(67,275, str(curso.descricao[:110]))
        PDF.drawString(67,250, str(curso.descricao[111:221]))
        PDF.drawString(67,225, str(curso.descricao[222:331]))
        PDF.drawString(67,200, str(curso.descricao[332:459]))
        PDF.drawString(67,175, str(curso.descricao[460:570]))

        PDF.showPage()
        PDF.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'Certificado({request.user}).pdf')
    except Exception as msg:
        print(msg)
        return