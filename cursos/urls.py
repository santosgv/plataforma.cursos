from django.urls import path
from . import views
from . import htmx_views

app_name = 'Curso'


urlpatterns = [
    path('', views.home, name = 'home'),
    path('sobre/', views.sobre, name = 'sobre'),
    path('contatos/', views.contatos, name = 'contatos'),
    path('cursos/',views.cursos,name='cursos'),
    path('curso/<int:id>', views.curso, name = 'curso'),
    path('aula/<int:id>', views.aula, name = 'aula'),
    path('verificar_progresso/<int:curso_id>',views.verificar_progresso, name='verificar_progresso'),
    path('baixar_certificado/<int:curso_id>',views.baixar_certificado,name='baixar_certificado'),
    path('processa_avaliacao/', views.processa_avaliacao, name = 'processa_avaliacao')
]

htmx_patterns =[
    path('comentar/<int:aula_id>',htmx_views.comentar, name='comentar'),
]

urlpatterns += htmx_patterns