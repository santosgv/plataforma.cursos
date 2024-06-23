
from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.messages import constants
from django.db import transaction
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

@transaction.atomic
def valida_cadastro(request):
    nome = request.POST.get('nome')
    first_name = request.POST.get('first_name')
    cpf = request.POST.get('cpf')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirm-password')
    
    if not senha == confirmar_senha:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
        return redirect('cadastro/')

    if USUARIO.objects.filter(email= email).exists():
        messages.add_message(request, constants.ERROR, 'Já existe um usário com esse username')
        return redirect('cadastro/')
    
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Os campos nao podem ser vazio')
        return redirect('cadastro/')
    
    if len(senha) < 8:
        messages.add_message(request, constants.ERROR, 'A senha deve ser maior que 8 caracteres')
        return redirect('cadastro/')
    
    try:
        
        usuario = USUARIO.objects.create_user(username = nome ,first_name=first_name,cpf=cpf, email = email, password = senha,)
        usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso!!!')
        return redirect('/login/')
    except:
        messages.add_message(request, constants.ERROR, 'Erro ao cadastrar o usuario entre em contato com o ADM')
        return redirect('cadastro/')

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
    

@transaction.atomic
def area_aluno(request):
    if request.method == "GET":
        username = request.user.username
        first_name = request.user.first_name
        cpf = request.user.cpf
        email = request.user.email

        return render(request,'area_aluno.html',{
                                                'username':username,
                                                'first_name':first_name,
                                                'cpf': cpf,
                                                'email':email
                                                    })
    else:
        
        usuario = request.user
        first_name = request.POST.get('first_name')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')


        if len(first_name.strip()) == 0  or len(cpf.strip()) == 0 or len(email.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/area_aluno.html')
        
        user = USUARIO.objects.filter(username=request.user).exclude(id=request.user.id)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usário com esse username')
            return redirect('/area_aluno.html')

        usuario = request.user
        usuario.first_name = first_name
        usuario.cpf = cpf
        usuario.email = email
        usuario.save()
        auth.logout(request)
    messages.add_message(request, constants.SUCCESS, 'Dados de Usuario Alterado com Sucesso, Faça novamente o Login para Validar')
    return redirect('/login')


def sair(request):
    request.session.flush()
    return redirect('/')

