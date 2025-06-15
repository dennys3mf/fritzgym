# maquinas/admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Maquina

# Usamos un decorador para registrar el modelo con nuestra clase personalizada
@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    """
    Personalización del panel de administrador para el modelo Maquina.
    """
    # Define las columnas que se mostrarán en la lista de máquinas
    list_display = ('nombre', 'ver_codigo_qr')

    def ver_codigo_qr(self, obj):
        """
        Crea una columna personalizada que contiene un enlace para ver el QR.
        'obj' es la instancia de la máquina de la fila actual.
        """
        # Usamos 'reverse' para construir la URL de forma segura a partir del nombre
        # que le dimos en urls.py ('generar-qr')
        url = reverse('generar-qr', args=[obj.id])

        # Creamos el enlace HTML. format_html previene problemas de seguridad.
        # target="_blank" hace que el enlace se abra en una nueva pestaña.
        return format_html('<a class="button" href="{}" target="_blank">Ver QR</a>', url)

    # Le damos un nombre legible a la columna en el panel de admin
    ver_codigo_qr.short_description = 'Código QR'
    # Permite ordenar por esta columna (aunque no tenga sentido aquí, es buena práctica)
    ver_codigo_qr.allow_tags = True

admin.site.site_header = "Fritz Gym Administración de Máquinas"
admin.site.site_title = "Panel de Fritz Gym"
admin.site.index_title = "Bienvenido al Administrador"