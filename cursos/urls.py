from django.urls import path
from . import views
from django.http.response import Http404
from django.http import HttpResponse

app_name = 'Curso'


urlpatterns = [
    path('', views.home, name = 'home'),
    path('cursos/',views.cursos,name='cursos'),
    path('curso/<int:id>', views.curso, name = 'curso'),
    path('aula/<int:id>', views.aula, name = 'aula'),
    path('verificar_progresso/<int:curso_id>',views.verificar_progresso, name='verificar_progresso'),
    path('comentarios/', views.comentarios, name = 'comentarios'),
    path('processa_avaliacao/', views.processa_avaliacao, name = 'processa_avaliacao')
]