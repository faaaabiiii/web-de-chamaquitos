from django import forms
from .models import *

class PublicarNoticia(forms.ModelForm):
    class Meta:
        model = Noticias
        fields = [
            "titulo", 
            "descripcion", 
            "url", 
            "url_img",
            ]