from django.shortcuts import get_object_or_404
from .models import ProgressoAula, Cursos,Aulas
from django.http import FileResponse
import io
import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def marcar_aula_concluida(usuario, aula_id):
    aula = get_object_or_404(Aulas, id=aula_id)
    progresso, created = ProgressoAula.objects.get_or_create(usuario=usuario, aula=aula)
    if not progresso.concluida:
        progresso.concluida = True
        progresso.save()

def calcular_progresso_curso(usuario, curso_id):
    curso = get_object_or_404(Cursos, id=curso_id)
    total_aulas = Aulas.objects.filter(curso=curso).count()
    aulas_concluidas = ProgressoAula.objects.filter(usuario=usuario, aula__curso=curso, concluida=True).count()
    
    if total_aulas == 0:
        return 0

    progresso = int((aulas_concluidas / total_aulas) * 100)
    return progresso

def pode_emitir_certificado(usuario, curso_id):
    progresso = calcular_progresso_curso(usuario, curso_id)
    return progresso >= 85


