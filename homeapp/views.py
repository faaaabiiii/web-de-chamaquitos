from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db import OperationalError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import requests
import json

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
                    "error": "El nombre de usuario ya existe"
                    })
        return render(request, "signup.html", {
            "form": UserCreationForm,
            "error": "Las contraseñas no coinciden"
            })

@login_required
def inicio(request):
    user = request.user
    if request.method == "GET":
        try:
            mis_noticias = Noticias.objects.filter(usuario=user).values()
            total_likes = 0
            total_compartidos = 0
            num_publicaciones = 0
            top = {'id':0, 'interacciones':0, 'titulo':""}
            for noticia in mis_noticias:
                num_publicaciones +=1
                total_likes += noticia['likes']
                total_compartidos += noticia['shared']
                if (noticia['likes'] + noticia['shared']) > top['interacciones']:
                    top['interacciones'] = noticia['likes'] + noticia['shared']
                    top['id'] = noticia['id']
                    top['titulo'] = noticia['titulo']
            context = {
                'form': PublicarNoticia,
                'user': user,
                'num_publicaciones': num_publicaciones,
                'total_likes': total_likes,
                'total_compartidos': total_compartidos,
                'top': top,
                }
            return render(request, "inicio.html", context)
        except OperationalError:
            context = {
                'form': PublicarNoticia,
                'user': user,
                'num_publicaciones': 0,
                'total_likes': total_likes,
                }
            return render(request, "inicio.html", context)
    if request.method == "POST":
        form = PublicarNoticia(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.usuario = request.user
            instancia.save()
            return redirect('comunidad')
        else:
            try:
                mis_noticias = Noticias.objects.filter(usuario=user).values()
                total_likes = 0
                total_compartidos = 0
                num_publicaciones = 0
                top = {'id':0, 'interacciones':0, 'titulo':""}
                for noticia in mis_noticias:
                    num_publicaciones +=1
                    total_likes += noticia['likes']
                    total_compartidos += noticia['shared']
                    if (noticia['likes'] + noticia['shared']) > top['interacciones']:
                        top['interacciones'] = noticia['likes'] + noticia['shared']
                        top['id'] = noticia['id']
                        top['titulo'] = noticia['titulo']
                context = {
                    'form': PublicarNoticia,
                    'user': user,
                    'num_publicaciones': num_publicaciones,
                    'total_likes': total_likes,
                    'total_compartidos': total_compartidos,
                    'top': top,
                    'error': "(*) Has ingresado datos incorrectos en las casillas, vuelve a intentarlo.",
                    }
                return render(request, "inicio.html", context)
            except OperationalError:
                context = {
                    'form': PublicarNoticia,
                    'user': user,
                    'num_publicaciones': 0,
                    'total_likes': 0,
                    'total_compartidos': 0,
                    'error': "(*) Has ingresado datos incorrectos en las casillas, vuelve a intentarlo.",
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
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('comunidad')
        
@login_required
@login_required
def mostrar_paisajes(request):
    # Lógica para mostrar paisajes
    return render(request, 'paisajes.html')

def mostrar_contadores(request):
    contadores = Paisajes.objects.get()
    return render(request, 'recorridos.html', {'contadores': contadores})

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

def news(request):
    if request.method == 'GET':
       url = "https://climate-news-feed.p.rapidapi.com/"
       querystring = {"limit":"50","exclude":"The Guardian"}
       headers = {
            "X-RapidAPI-Key": "9acd896290mshd7266af432403dcp12ac41jsn0b84bdd47bfa",
            "X-RapidAPI-Host": "climate-news-feed.p.rapidapi.com"
       }
       response = requests.get(url, headers=headers, params=querystring)
       news = response.json()
       context = {
            'noticias': news
        }
       return render(request, "news.html", context)
        



@login_required
def afectados(request):
    return render(request, 'paisajes.html')
    
def comunidad(request):
    user = request.user
    noticias = Noticias.objects.all()
    if noticias.exists():
        return render(request, 'comunidad.html',{'noti': noticias , 'user': user, 'flag': 1})
    else:
        return render(request, 'comunidad.html',{'noti': noticias , 'user': user, 'flag': 0})

@login_required
def agregar_like(request, id, user):
    noticia = Noticias.objects.get(id=id)
    if user not in noticia.laikeros:
        noticia.likes += 1
        noticia.laikeros.append(user) 
        noticia.save()
    else:
        noticia.likes -= 1
        noticia.laikeros.remove(user)
        noticia.save()
    return redirect('/comunidad')

def nosotros(request):
    return render(request, "nosotros.html")

@login_required
def misnoticias(request):
    user = request.user
    try:
        post = Noticias.objects.filter(usuario=user).values()
        if post.exists():
            return render(request, "misnoticias.html", {'post': post})
        else:
            return render(request, "misnoticias.html", {'post': "nohay", 'error': "* No has publicado una noticia aún."})
    
    
    except OperationalError:
        return render(request, "misnoticias.html", {'post': None, 'error': "* No has publicado una noticia aún."})

@login_required
def unasola(request, id):
    if request.method == 'GET':
        una = get_object_or_404(Noticias, pk=id)
        form = PublicarNoticia(instance=una)
        return render(request, "una.html", {'una': una, 'form': form})
    else:
        try:
            una = get_object_or_404(Noticias, pk=id)
            form = PublicarNoticia(request.POST, instance=una)
            form.save() 
            return redirect('misnoticias')
        except ValueError:
            return render(request, "una.html", {'una': una, 'form': form, 'error': "Error updating post"})

@login_required        
def delete(request, id):
    noti = get_object_or_404(Noticias, pk= id)
    if request.method == "POST":
        noti.delete()
        return redirect('misnoticias') 