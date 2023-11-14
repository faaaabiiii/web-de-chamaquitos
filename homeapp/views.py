from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError 
from django.db import OperationalError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Create your views here.

def home(request):
    return render(request, "home.html")

def signup(request):

    if request.method == "GET":
        return render(request, "signup.html", {
            "form": UserCreationForm
             })
    
    else:
        if request.POST["password1"] == request.POST["password2"]:
            #reguster user
            try:
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("inicio")
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "username already exists"
                    })
        return render(request, "signup.html", {
            "form": UserCreationForm,
            "error": "Password do not match"
            })

@login_required
def inicio(request):
    form = PublicarNoticia(request.POST or None)
    if form.is_valid():
        instancia = form.save(commit=False)
        instancia.usuario = request.user
        instancia.save()
        form = PublicarNoticia()
        return redirect('comunidad')
    context = {
        'form': form
    }
    return render(request, "inicio.html", context)

@login_required
def signout(request):
    logout(request)
    return redirect('home') 

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
            })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('inicio')
        
@login_required
@login_required
def mostrar_paisajes(request):
    # Lógica para mostrar paisajes
    return render(request, 'paisajes.html')

def mostrar_contadores(request):
    contadores = Paisajes.objects.get()
    return render(request, 'paisajes.html', {'contadores': contadores})

def incrementar_contador(request, contador_id):
    try:
        contador = Paisajes.objects.get()
    except Paisajes.DoesNotExist:
        return render(request, 'error.html', {'error': 'No se encontró el objeto Contador en la base de datos'})

    if contador_id == 1:
        contador.contador1 += 1
    elif contador_id == 2:
        contador.contador2 += 1
    contador.save()

    return redirect('mostrar_contadores')  # Redirige después de incrementar el contador

@login_required
def news(request):
    if request.method == 'POST':
        shared = Noticias.objects.get()
        shared.shared += 1
        shared.save()
        return render(request, 'news.html', 
                      {'form': PublicarNoticia()})
    
    else:
        return render(request, 'news.html', 
                      {'form': PublicarNoticia()})

@login_required
def afectados(request):
    return render(request, 'paisajes.html')
    
def comunidad(request):
    noticias = Noticias.objects.all()
    return render(request, 'comunidad.html',{'noti': noticias })

def nosotros(request):
    return render(request, "nosotros.html")

def Mipost(request):
    user = request.user
    try:
        post = Noticias.objects.filter(usuario=user).values()
        return render(request, "mipost.html", {'post': post})
    except OperationalError:
        return render(request, "mipost.html", {'post': None, 'error': "* No has publicado una noticia aún."})

