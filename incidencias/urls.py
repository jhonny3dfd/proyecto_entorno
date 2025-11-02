<<<<<<< HEAD
# incidencias/urls.py (CONTENIDO COMPLETO DEL ARCHIVO)

from django.urls import path
from .views import (
    SolicitudListView,
    SolicitudDetailView,
    SolicitudCreateView,
    ResolucionCreateView,
    SolicitudUpdateView, # <-- IMPORTAR
    toggle_encuesta_status, # <-- IMPORTAR
)
=======
from django.contrib import admin
from django.urls import path, include

# incidencias/urls.py

from django.urls import path
from .views import SolicitudListView, SolicitudDetailView, SolicitudCreateView # <--- Importar SolicitudCreateView
>>>>>>> 29efc874b2544b2b93fd82a96d1864161b6d4137

incidencias_urlpatterns = [
    # Listado
    path('incidencias/', SolicitudListView.as_view(), name='solicitud_list'),
<<<<<<< HEAD

    # Creación (ya existe)
    path('incidencias/crear/', SolicitudCreateView.as_view(), name='solicitud_create'),

    # Detalle (ya existe)
    path('incidencias/<int:pk>/', SolicitudDetailView.as_view(), name='solicitud_detail'),

    # Resolución (ya existe)
    path('incidencias/<int:pk>/resolver/', ResolucionCreateView.as_view(), name='solicitud_resolver'),

    # Edición de Solicitud/Encuesta
    path('incidencias/<int:pk>/editar/', SolicitudUpdateView.as_view(), name='solicitud_update'), # <-- NUEVA URL

    # Activar/Bloquear Encuesta
    path('incidencias/<int:pk>/encuesta/estado/', toggle_encuesta_status, name='encuesta_toggle_status'), # <-- NUEVA URL
=======
    
    # NUEVA URL DE CREACIÓN
    path('incidencias/crear/', SolicitudCreateView.as_view(), name='solicitud_create'), # <--- Nuevo

    # Detalle
    path('incidencias/<int:pk>/', SolicitudDetailView.as_view(), name='solicitud_detail'),
>>>>>>> 29efc874b2544b2b93fd82a96d1864161b6d4137
]