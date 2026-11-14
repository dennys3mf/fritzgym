from django.db import models
import re
from urllib.parse import parse_qs, urlparse

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

    def __str__(self):
        return self.nombre

    @property
    def youtube_id(self):
        parsed = urlparse(self.url_video or '')
        hostname = (parsed.hostname or '').lower()
        if parsed.scheme != 'https':
            return ''
        if hostname in {'youtu.be', 'www.youtu.be'}:
            candidate = parsed.path.strip('/')
        elif hostname in {'youtube.com', 'www.youtube.com', 'm.youtube.com',
                          'youtube-nocookie.com', 'www.youtube-nocookie.com'}:
            parts = parsed.path.strip('/').split('/')
            candidate = parts[1] if len(parts) == 2 and parts[0] in {'embed', 'shorts'} else (
                parse_qs(parsed.query).get('v', [''])[0] if parsed.path == '/watch' else '')
        else:
            return ''
        return candidate if re.fullmatch(r'[a-zA-Z0-9_-]{11}', candidate) else ''

    @property
    def video_embed_url(self):
        return f'https://www.youtube.com/embed/{self.youtube_id}?rel=0' if self.youtube_id else ''

    @property
    def video_watch_url(self):
        return f'https://www.youtube.com/watch?v={self.youtube_id}' if self.youtube_id else ''

    @property
    def thumbnail_url(self):
        yid = self.youtube_id
        if yid:
            return f"https://img.youtube.com/vi/{yid}/hqdefault.jpg"
        return ""


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
