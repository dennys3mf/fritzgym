from django import forms
from django.contrib import admin, messages
from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from .models import Anuncio, Maquina


class MaquinaAdminForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = '__all__'
        labels = {'nombre': 'Nombre de la máquina', 'grupo_muscular': 'Grupo muscular',
                  'url_video': 'Enlace del tutorial', 'descripcion': 'Guía de ejecución'}
        help_texts = {
            'nombre': 'Usa el nombre que las personas reconocen en la sala.',
            'grupo_muscular': 'Determina en qué filtro aparece la ficha del catálogo.',
            'url_video': 'Pega un enlace de YouTube: video normal, enlace corto o Shorts.',
            'descripcion': 'Explica el ajuste del equipo, la ejecución y los errores que conviene evitar. Puedes separar los pasos con saltos de línea.',
        }
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 12, 'class': 'vLargeTextField'}),
                   'url_video': forms.URLInput(attrs={'placeholder': 'https://www.youtube.com/watch?v=…'})}

    def clean_url_video(self):
        value = self.cleaned_data.get('url_video', '').strip()
        machine = Maquina(url_video=value)
        if value and not machine.youtube_id:
            raise forms.ValidationError('Introduce un enlace válido de YouTube. Revisa que incluya el identificador completo del video.')
        return f'https://www.youtube.com/embed/{machine.youtube_id}' if value else value


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    form = MaquinaAdminForm
    list_display = ('nombre', 'grupo_visible', 'estado_ficha', 'ver_ficha', 'ver_codigo_qr')
    list_display_links = ('nombre',)
    list_filter = ('grupo_muscular',)
    search_fields = ('nombre', 'descripcion')
    search_help_text = 'Busca por nombre o por una palabra de la guía de ejecución.'
    ordering = ('nombre',)
    list_per_page = 25
    empty_value_display = 'Sin completar'
    readonly_fields = ('vista_previa_video', 'accesos_publicos')
    fieldsets = (
        ('Identificación en sala', {'fields': ('nombre', 'grupo_muscular'),
                                  'description': 'Estos datos identifican la ficha y la organizan en el catálogo.'}),
        ('Video y técnica', {'fields': ('url_video', 'vista_previa_video', 'descripcion')}),
        ('Ficha pública y código QR', {'fields': ('accesos_publicos',),
                                      'description': 'Los enlaces conservan su dirección cuando editas esta máquina.'}),
    )

    @admin.display(description='Grupo muscular', ordering='grupo_muscular')
    def grupo_visible(self, obj):
        return format_html('<span class="admin-tag">{}</span>', obj.get_grupo_muscular_display())

    @admin.display(description='Contenido')
    def estado_ficha(self, obj):
        if not obj.youtube_id:
            return format_html('<span class="admin-status admin-status-warning">{}</span>', 'Revisar enlace')
        if not obj.descripcion.strip():
            return format_html('<span class="admin-status admin-status-warning">{}</span>', 'Falta la guía')
        return format_html('<span class="admin-status">{}</span>', 'Video y guía')

    @admin.display(description='Vista pública')
    def ver_ficha(self, obj):
        return format_html('<a class="admin-inline-link" href="{}" target="_blank" rel="noopener noreferrer">Ver ficha</a>',
                           reverse('detalle-maquina', args=[obj.pk]))

    @admin.display(description='Código QR')
    def ver_codigo_qr(self, obj):
        return format_html('<a class="admin-inline-link" href="{}" target="_blank" rel="noopener noreferrer">Abrir QR</a>',
                           reverse('generar-qr', args=[obj.pk]))

    @admin.display(description='Vista previa')
    def vista_previa_video(self, obj):
        if not obj or not obj.youtube_id:
            return format_html('<div class="admin-video-preview" id="admin-video-preview"><p>{}</p></div>',
                               'Pega un enlace para ver la vista previa del tutorial.')
        return format_html(
            '<div class="admin-video-preview" id="admin-video-preview">'
            '<img src="{}" alt="Miniatura del tutorial" width="320" height="180" loading="lazy">'
            '<div><strong>Tutorial vinculado</strong><p>Comprueba que el ejercicio corresponde a esta máquina.</p>'
            '<a href="{}" target="_blank" rel="noopener noreferrer">Ver en YouTube</a></div></div>',
            obj.thumbnail_url, obj.video_watch_url)

    @admin.display(description='Accesos')
    def accesos_publicos(self, obj):
        if not obj or not obj.pk:
            return 'La ficha y el código QR estarán disponibles después de guardar la máquina.'
        return format_html(
            '<div class="admin-public-links"><a class="button" href="{}" target="_blank" rel="noopener noreferrer">Ver ficha pública</a>'
            '<a class="button admin-button-secondary" href="{}" target="_blank" rel="noopener noreferrer">Abrir código QR</a></div>',
            reverse('detalle-maquina', args=[obj.pk]), reverse('generar-qr', args=[obj.pk]))


@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estado_publicacion', 'activo', 'fecha_creacion')
    list_display_links = ('titulo',)
    list_editable = ('activo',)
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('titulo', 'contenido')
    search_help_text = 'Busca un anuncio por su título o por su contenido.'
    readonly_fields = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)
    list_per_page = 25
    actions = ('publicar_anuncios', 'ocultar_anuncios')
    fieldsets = (
        ('Contenido del anuncio', {'fields': ('titulo', 'contenido'),
                                  'description': 'El título y el mensaje se muestran en la página principal.'}),
        ('Imagen y enlace', {'fields': ('imagen_anuncio', 'enlace_opcional'),
                            'description': 'Opcionales. Añade una imagen y un enlace de información cuando sean necesarios.'}),
        ('Publicación', {'fields': ('activo', 'fecha_creacion'),
                        'description': 'Un anuncio activo es visible en la web. Desactívalo para ocultarlo sin eliminarlo.'}),
    )
    formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'rows': 7})}}

    @admin.display(description='Estado', ordering='activo')
    def estado_publicacion(self, obj):
        return format_html('<span class="admin-status {}">{}</span>',
                           '' if obj.activo else 'admin-status-neutral',
                           'Publicado' if obj.activo else 'Oculto')

    @admin.action(description='Publicar los anuncios seleccionados', permissions=['change'])
    def publicar_anuncios(self, request, queryset):
        count = queryset.update(activo=True)
        self.message_user(request, f'{count} anuncio(s) publicado(s).', messages.SUCCESS)

    @admin.action(description='Ocultar los anuncios seleccionados', permissions=['change'])
    def ocultar_anuncios(self, request, queryset):
        count = queryset.update(activo=False)
        self.message_user(request, f'{count} anuncio(s) oculto(s).', messages.SUCCESS)


admin.site.site_header = 'Fritz Gym'
admin.site.site_title = 'Administración de Fritz Gym'
admin.site.index_title = 'Panel de control'
admin.site.index_template = 'admin/fritz_index.html'
admin.site.login_template = 'admin/fritz_login.html'
