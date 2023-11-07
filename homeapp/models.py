from django.db import models

class Noticia2(models.Model):
    title = models.CharField(max_length=50)
    likes = models.IntegerField()
    shared = models.IntegerField()
    
    def __str__(self):
        return self.title

class Paisaje2(models.Model):
    title = models.CharField(max_length=50)
    likes = models.IntegerField()
    shared = models.IntegerField()

    def __str__(self):
        return self.title