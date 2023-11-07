from django import forms

class Noticia1(forms.Form):
    titulo =  forms.CharField(max_length=50, required=True)
    descripcion = forms.CharField(max_length=200, required=False)
    url = forms.CharField(max_length=300, required=True)
    url_img = forms.CharField(max_length=300, required=False)
    likes = forms.IntegerField(required=False)
    shared = forms.IntegerField(required=False)

class Paisaje1(forms.Form):
    nombre =  forms.CharField(max_length=50, required=False)
    likes = forms.IntegerField(required=False)
    shared = forms.IntegerField(required=False)