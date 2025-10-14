from django.contrib import admin
from django.urls import path, include

# incidencias/urls.py

from django.urls import path
from .views import SolicitudListView, SolicitudDetailView, SolicitudCreateView # <--- Importar SolicitudCreateView

incidencias_urlpatterns = [
    # Listado
    path('incidencias/', SolicitudListView.as_view(), name='solicitud_list'),
    
    # NUEVA URL DE CREACIÓN
    path('incidencias/crear/', SolicitudCreateView.as_view(), name='solicitud_create'), # <--- Nuevo

    # Detalle
    path('incidencias/<int:pk>/', SolicitudDetailView.as_view(), name='solicitud_detail'),
]