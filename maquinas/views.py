# maquinas/views.py

# --- Importaciones limpias y ordenadas ---
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from io import BytesIO
import qrcode
from .models import Maquina

# ----------------------------------------------

def lista_maquinas(request):
    """Muestra la página principal con la lista de todas las máquinas."""
    maquinas = Maquina.objects.all()
    contexto = {
        'maquinas_list': maquinas
    }
    return render(request, 'maquinas/lista_maquinas.html', contexto)

def detalle_maquina(request, maquina_id):
    """Muestra la página de detalle para una sola máquina."""
    maquina = get_object_or_404(Maquina, pk=maquina_id)
    contexto = {
        'maquina': maquina,
    }
    return render(request, 'maquinas/detalle_maquina.html', contexto)

def generar_qr(request, maquina_id):
    """Genera una imagen de QR que apunta a la página de detalle de una máquina."""
    
    # 1. Construimos la URL a la vista de DETALLE de forma profesional
    url_detalle = reverse('detalle-maquina', args=[maquina_id])
    url_absoluta = request.build_absolute_uri(url_detalle)

    # 2. Generamos el código QR con la URL CORRECTA (url_absoluta)
    qr_imagen = qrcode.make(url_absoluta, box_size=15, border=1)

    # 3. Guardamos la imagen en memoria
    buffer = BytesIO()
    qr_imagen.save(buffer, 'PNG')
    buffer.seek(0)

    # 4. Devolvemos la imagen como una respuesta HTTP
    return HttpResponse(buffer, content_type='image/png')

def pagina_sobre_nosotros(request):
    return render(request, 'maquinas/sobre_nosotros.html')

def pagina_contacto(request):
    return render(request, 'maquinas/contacto.html')

def pagina_privacidad(request):
    return render(request, 'maquinas/privacidad.html')