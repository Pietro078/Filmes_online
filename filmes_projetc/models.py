from django.db import models

# Create your models here.
class Filmes(models.Model):
    id = models.IntegerField(primary_key=True, blank=False)
    nome = models.CharField(max_length=100, blank=False)
    genero = models.CharField(max_length=100, blank=True)
    tamb = models.CharField(max_length=50, null=True)
    sinopse = models.CharField(max_length=400, null=True)
    data_filme = models.CharField(max_length=15, null=True)
    
    def __str__(self):
        return self.nome

class MagnetcLinks(models.Model):
    id = models.IntegerField( primary_key=True)
    link_1080p_dub = models.CharField(max_length=100, blank=True)
    link_720p_dub = models.CharField(max_length=100, blank=True)
    link_1080p_eng = models.CharField(max_length=100, blank=True)
    link_720p_eng = models.CharField(max_length=100, blank=True)

class link_series(models.Model):
    id = models.IntegerField( primary_key=True)
    link_eps = models.CharField(max_length=100, blank=True)
    ep_name = models.CharField(max_length=20, blank=True, null=True)

