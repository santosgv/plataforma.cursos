from django.utils.timezone import now
import io
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,landscape
from django.http import FileResponse,HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import  render,redirect,get_object_or_404
from .models import Comentarios, Cursos,Aulas, NotasAulas, ProgressoAula,Contato
from usuarios.models import USUARIO
from django.db import transaction
from .utils import marcar_aula_concluida, calcular_progresso_curso, pode_emitir_certificado
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
import logging

logger = logging.getLogger('Aplicacao')

@login_required
def verificar_progresso(request, curso_id):
    curso = Cursos.objects.get(id=curso_id)
    progresso = calcular_progresso_curso(request.user, curso_id)
    certificado_disponivel = pode_emitir_certificado(request.user, curso_id)
    return render(request, 'progresso.html', {'curso': curso, 'progresso': progresso, 'certificado_disponivel': certificado_disponivel})

@login_required
def home(request):
    return render(request, 'home.html')

def contatos(request):
    if request.method == "GET":
        return render(request, 'contact.html')
    else:
        NOME = request.POST.get('name')
        EMAIL = request.POST.get('email')
        ASSUNTO = request.POST.get('subject')
        MENSAGEM = request.POST.get('message')
        
        new_contato= Contato(
            Nome=NOME,
            Email=EMAIL,
            assunto=ASSUNTO,
            Mensagem=MENSAGEM
        )
        new_contato.save()
        messages.add_message(request, constants.SUCCESS, 'Enviado com sucesso')
        return redirect('/home/contatos')

def sobre(request):
    return render(request, 'about.html')

@login_required
def cursos(request):
    paginas_cursos=Cursos.objects.all().filter(ativo=True).order_by('nome').only('nome','descricao','thumb')
    pagina = Paginator(paginas_cursos, 25)
    page = request.GET.get('page')
    cursos = pagina.get_page(page)
    return render(request, 'cursos.html', {'cursos': cursos,})

@login_required
def curso(request, id):
    paginas_aulas = Aulas.objects.filter(curso = id).filter(ativo=True).order_by('nome').only('nome','descricao','data_upload')
    avaliacoes = NotasAulas.objects.filter(aula_id = id).only('nota','usuario')
    pagina = Paginator(paginas_aulas, 25)
    page = request.GET.get('page')
    aulas = pagina.get_page(page)
    return render(request, 'curso.html', {'aulas': aulas,
                                        'avaliacoes': avaliacoes})

@login_required
def aula(request, id):

    aula = Aulas.objects.get(id = id)
    comentarios = Comentarios.objects.filter(aula = aula).order_by('-data').only('usuario','comentario','data')
    usuario_avaliou = NotasAulas.objects.filter(aula_id = id).filter(usuario_id = request.user.id)
    avaliacoes = NotasAulas.objects.filter(aula_id = id)

    
    marcar_aula_concluida(request.user, aula.id)
    return render(request, 'aula.html', {'aula': aula,
                                        'usuario_id': request.user.id,
                                        'comentarios': comentarios,
                                        'request_usuario': request.user,
                                        'usuario_avaliou': usuario_avaliou,
                                        'avaliacoes': avaliacoes})


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
        return redirect('/cursos')
    

@transaction.atomic
@login_required
def baixar_certificado(request, aluno_id, curso_id):
    if not request.user.is_gestor:
        return HttpResponseForbidden("Você não tem permissão para baixar este certificado.")

    aluno = get_object_or_404(USUARIO, id=aluno_id)
    curso = get_object_or_404(Cursos, id=curso_id)
    
    if not aluno in request.user.alunos.all():
        return HttpResponseForbidden("Você não tem permissão para baixar o certificado deste aluno.")
    
    if not pode_emitir_certificado(aluno, curso_id):
        return HttpResponseForbidden("O aluno não possui progresso suficiente para emitir o certificado.")

    progresso = ProgressoAula.objects.filter(usuario=aluno, aula__curso=curso_id).first()
    progresso.baixou_certificado = True
    progresso.save()

    progresso.data_certificado = now()
    progresso.save()
    try:
        buffer = io.BytesIO()
        PDF = canvas.Canvas(buffer, pagesize=landscape(letter))
        PDF.setFont('Times-Roman', 30)
        image_path = os.path.join(settings.BASE_DIR, 'templates', 'certificado.jpeg')
        PDF.drawImage(image_path, 0, 0, width=landscape(letter)[0], height=landscape(letter)[1])
        PDF.drawString(230,390,str(aluno.first_name))
        PDF.setFont('Times-Roman', 20)
        PDF.drawString(395,359,str(aluno.cpf))
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
        
        if os.path.exists(f'certificados/{aluno.username}-{curso_id}.pdf'):
            print('ja existe')
        else:
            with open(os.path.join(settings.MEDIA_ROOT,f'certificados/{aluno.username}-{curso_id}.pdf'), 'wb') as f:
                f.write(buffer.getvalue())
                progresso.link_certificado = f'{settings.MEDIA_URL}certificados/{aluno.username}-{curso_id}.pdf'
                progresso.save()
        return FileResponse(buffer, as_attachment=True, filename=f'Certificado({aluno.username}).pdf')
    except Exception as e:
        logger.exception('Erro ao gerar o Certificado: %s', e)
        return redirect('/login')
    
@cache_page(60 * 100)
def politica(request):
     return render(request,'politica-de-privacidade.html')

@cache_page(60 * 100)
def transparencia(request):
     return render(request,'transparencia.html')