from django.urls import path
from . import views

app_name = 'Usuario'

urlpatterns = [
    path('', views.principal, name = 'principal'),
    path('area_aluno/',views.area_aluno, name='area_aluno'),
    path('cadastro/', views.cadastro, name = 'cadastro'),
    path('login/', views.login, name = 'login'),
    path('valida_cadastro/', views.valida_cadastro, name = 'valida_cadastro'),
    path('valida_login/', views.valida_login, name = 'valida_login'),
    path('sair/', views.sair, name = 'sair'),
] 