from django import forms

class Noticia1(forms.Form):
    nombre =  forms.CharField(max_length=50, required=False)
    descripcion = forms.CharField(max_length=200, required=False)
    likes = forms.IntegerField(required=False)
    shared = forms.IntegerField(required=False)

class Paisaje1(forms.Form):
    nombre =  forms.CharField(max_length=50, required=False)
    likes = forms.IntegerField(required=False)
    shared = forms.IntegerField(required=False)