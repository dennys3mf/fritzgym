from django.db import models

# Create your models here.
class Maquina(models.Model):
    # --- Opciones predefinidas para los grupos musculares ---
    class GrupoMuscular(models.TextChoices):
        PECHO = 'PE', 'Pecho'
        ESPALDA = 'ES', 'Espalda'
        PIERNA = 'PI', 'Pierna'
        BRAZO = 'BR', 'Brazo'
        HOMBRO = 'HO', 'Hombro'
        ABDOMEN = 'AB', 'Abdomen'
        OTRO = 'OT', 'Otro'

    # --- Campos del modelo ---
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    url_video = models.URLField(max_length=200)

    # --- NUEVO CAMPO AÑADIDO ---
    grupo_muscular = models.CharField(
        max_length=2,
        choices=GrupoMuscular.choices,
        default=GrupoMuscular.OTRO,
        help_text="Selecciona el grupo muscular principal que trabaja esta máquina."
    )
class Anuncio(models.Model):
    titulo = models.CharField(max_length=150)
    contenido = models.TextField(help_text="El texto principal del anuncio.")
    enlace_opcional = models.URLField(blank=True, null=True, help_text="Un enlace si el anuncio lleva a otra página (ej: a un formulario de inscripción).")
    imagen_anuncio = models.ImageField(upload_to='anuncios/', blank=True, null=True, help_text="Una imagen promocional.")
    activo = models.BooleanField(default=True, help_text="Desmarca esta casilla para ocultar el anuncio sin borrarlo.")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Anuncio"
        verbose_name_plural = "Anuncios"
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return self.nombre