from django.db import models

# Create your models here.
class Maquina(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    url_video = models.URLField(max_length=200)

    def __str__(self):
        return self.nombre