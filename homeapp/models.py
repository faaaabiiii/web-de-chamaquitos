from django.db import models


class Noticias(models.Model):
    titulo = models.CharField(max_length=50, blank=False)
    descripcion = models.CharField(max_length=200, blank=False)
    url = models.URLField(blank=False)
    url_img = models.URLField(blank=False)
    likes = models.IntegerField(null=True, blank=True)
    shared = models.IntegerField(null=True, blank=True)
    usuario = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.titulo

class Paisajes(models.Model):
    contador1 = models.IntegerField(default=0)
    contador2 = models.IntegerField(default=0)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title