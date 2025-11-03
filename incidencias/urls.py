# incidencias/urls.py (CONTENIDO COMPLETO DEL ARCHIVO)

from django.urls import path
from .views import (
    SolicitudListView,
    SolicitudDetailView,
    SolicitudCreateView,
    ResolucionCreateView,
    SolicitudUpdateView, 
    toggle_encuesta_status, 
)
from django.contrib import admin
from django.urls import path, include


from django.urls import path
from .views import SolicitudListView, SolicitudDetailView, SolicitudCreateView 
incidencias_urlpatterns = [
    path('incidencias/', SolicitudListView.as_view(), name='solicitud_list'),

    path('incidencias/crear/', SolicitudCreateView.as_view(), name='solicitud_create'),

    path('incidencias/<int:pk>/', SolicitudDetailView.as_view(), name='solicitud_detail'),

    path('incidencias/<int:pk>/resolver/', ResolucionCreateView.as_view(), name='solicitud_resolver'),

    path('incidencias/<int:pk>/editar/', SolicitudUpdateView.as_view(), name='solicitud_update'), 

    path('incidencias/<int:pk>/encuesta/estado/', toggle_encuesta_status, name='encuesta_toggle_status'), 
    
    path('incidencias/crear/', SolicitudCreateView.as_view(), name='solicitud_create'), 

    path('incidencias/<int:pk>/', SolicitudDetailView.as_view(), name='solicitud_detail'),
]