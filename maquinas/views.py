from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django.db.models import Q # <-- AÑADE ESTA IMPORTACIÓN
from io import BytesIO
import qrcode
from .models import Maquina, Anuncio # <-- Asegúrate que Anuncio esté aquí
from .catalogo import GRUPOS, obtener_guia

def lista_maquinas(request):
    """
    Muestra la lista de máquinas, con capacidad de búsqueda y filtro.
    """
    # Obtenemos la lista completa de máquinas para empezar
    queryset = Maquina.objects.all()

    # Obtenemos los parámetros de la URL (si existen)
    query = request.GET.get('q')
    grupo_filtrado = request.GET.get('grupo')

    # Si hay un parámetro de búsqueda 'q', filtramos el queryset
    if query:
        queryset = queryset.filter(
            Q(nombre__icontains=query) |  # type: ignore
            Q(descripcion__icontains=query)
        ).distinct()

    # Si hay un parámetro de filtro 'grupo', filtramos el queryset
    if grupo_filtrado:
        queryset = queryset.filter(grupo_muscular=grupo_filtrado)

    # Obtenemos los anuncios activos
    anuncios_activos = Anuncio.objects.filter(activo=True)

    # Obtenemos todos los grupos musculares para mostrar los botones de filtro
    grupos_musculares = Maquina.GrupoMuscular.choices

    contexto = {
        'maquinas_list': queryset, # Le pasamos el queryset ya filtrado
        'anuncios_activos': anuncios_activos,
        'grupos_musculares': grupos_musculares, # Pasamos los grupos para los botones
        'query_busqueda': query or "", # Pasamos el término de búsqueda para mostrarlo en la barra
        'grupo_actual': GRUPOS.get(grupo_filtrado),
    }
    return render(request, 'maquinas/lista_maquinas.html', contexto)

def detalle_maquina(request, maquina_id):
    """Muestra la página de detalle para una sola máquina."""
    maquina = get_object_or_404(Maquina, pk=maquina_id)
    contexto = {
        'maquina': maquina,
        'guia': obtener_guia(maquina),
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
