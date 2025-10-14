from django.contrib import admin
from django.urls import path, include
from .views import DireccionListView, DireccionDetailView, DepartamentoDetailView

organizacion_urlpatterns=[# organizacion/urls.py

    # Listado de Direcciones
    path('direcciones/', DireccionListView.as_view(), name='direccion_list'),
    
    # Detalle de Dirección (usa el campo 'pk' para identificarla)
    path('direcciones/<int:pk>/', DireccionDetailView.as_view(), name='direccion_detail'),
    
    # Detalle de Departamento (opcional, para ver un departamento específico)
    path('departamentos/<int:pk>/', DepartamentoDetailView.as_view(), name='departamento_detail'),
]
    
