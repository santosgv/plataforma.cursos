
from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.messages import constants
#from django.contrib.auth.models import User
from .models import USUARIO
from django.contrib import auth

def principal(request):
    return render(request,'principal.html')

def cadastro(request):
    if request.session.get('usuario'):
        return redirect('/home/')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

def login(request):
    if request.session.get('usuario'):
        return redirect('/home/')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    first_name = request.POST.get('first_name')
    cpf = request.POST.get('cpf')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirm-password')
    
    if not senha == confirmar_senha:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
        return redirect('/auth/cadastro')

    if USUARIO.objects.filter(email= email).exists():
        messages.add_message(request, constants.ERROR, 'Já existe um usário com esse username')
        return redirect('/auth/cadastro')
    
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Os campos nao podem ser vazio')
        return redirect('/auth/cadastro')
    
    if len(senha) < 8:
        messages.add_message(request, constants.ERROR, 'A senha deve ser maior que 8 caracteres')
        return redirect('/auth/cadastro')
    
    try:
        
        usuario = USUARIO.objects.create_user(username = nome ,first_name=first_name,cpf=cpf, email = email, password = senha,)
        usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso!!!')
        return redirect('/login/')
    except:
        messages.add_message(request, constants.ERROR, 'Erro ao cadastrar o usuario entre em contato com o ADM')
        return redirect('/auth/cadastro')

def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    

    usuarios = auth.authenticate(request, username= nome, password = senha)

    if not usuarios:
        messages.add_message(request, constants.ERROR, 'Usuario ou senha estao incorretos')
        return redirect('/login')
    else:
        auth.login(request,usuarios)
        return redirect('/home')

def area_aluno(request):
    return render(request,'area_aluno.html')

def sair(request):
    request.session.flush()
    return redirect('/')

