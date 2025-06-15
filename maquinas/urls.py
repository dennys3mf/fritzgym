from django.urls import path
from . import views  # Importamos el archivo views.py de esta misma carpeta

urlpatterns = [
    # Cuando alguien visite la URL raíz (''), se ejecutará la función lista_maquinas
    path('', views.lista_maquinas, name='lista-maquinas'),
    path('maquina/<int:maquina_id>/', views.detalle_maquina, name='detalle-maquina'), # <-- AÑADE ESTA LÍNEA
    path('maquina/<int:maquina_id>/qr/', views.generar_qr, name='generar-qr'),

]