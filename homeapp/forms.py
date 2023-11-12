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
        
class Paisaje1(forms.Form):
    nombre =  forms.CharField(max_length=50, required=False)
    likes = forms.IntegerField(required=False)
    shared = forms.IntegerField(required=False)