
from django.shortcuts import render,redirect
from .models import Usuario
from django.contrib.auth.models import User
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
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    
    

    if User.objects.filter(email= email).exists():
        return redirect('/auth/cadastro/?status=1')
    
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=2')
    
    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=3')
    
    try:
        
        usuario = User.objects.create_user(username = nome , email = email, password = senha)
        usuario.save()
        return redirect('/auth/cadastro/?status=0')
    except:
        return redirect('/auth/cadastro/?status=4')

def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    

    usuarios = auth.authenticate(request, username= nome, password = senha)

    if not usuarios:
        return redirect('/auth/login/?status=1')
    else:
        auth.login(request,usuarios)
        return redirect('/home')

def sair(request):
    request.session.flush()
    return redirect('/auth/login/')

