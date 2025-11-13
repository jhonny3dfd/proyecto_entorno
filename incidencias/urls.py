# incidencias/urls.py (Contenido Completo)

from django.urls import path
from .views import (
    SolicitudListView,
    SolicitudDetailView,
    SolicitudCreateView,
    ResolucionCreateView,
    SolicitudUpdateView, 
    SolicitudDerivarView,
    # Asegúrate de importar esta función
    toggle_encuesta_status, 
)

incidencias_urlpatterns = [
    # Listado
    path('incidencias/', SolicitudListView.as_view(), name='solicitud_list'),

    # Creación
    path('incidencias/crear/', SolicitudCreateView.as_view(), name='solicitud_create'),

    # Detalle (donde falla el botón)
    path('incidencias/<int:pk>/', SolicitudDetailView.as_view(), name='solicitud_detail'),

    # Resolución
    path('incidencias/<int:pk>/resolver/', ResolucionCreateView.as_view(), name='solicitud_resolver'),

    # Edición de Solicitud/Encuesta
    path('incidencias/<int:pk>/editar/', SolicitudUpdateView.as_view(), name='solicitud_update'), 

    # 🚨 LÍNEA CRÍTICA: Definición de la URL faltante (o mal nombrada)
    path('incidencias/<int:pk>/toggle_encuesta/', toggle_encuesta_status, name='toggle_encuesta_status'), 

    path('incidencias/<int:pk>/derivar/', SolicitudDerivarView.as_view(), name='solicitud_derivar'), # <--- 🚨 NUEVA RUTA 🚨
]

# Si usas un patrón diferente para incluir las URLs en tu proyecto principal, 
# asegúrate de que el nombre 'toggle_encuesta_status' se mantenga.