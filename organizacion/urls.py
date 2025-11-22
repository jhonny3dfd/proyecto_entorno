# organizacion/urls.py

from django.urls import path
from .views import (
    DireccionListView, DireccionDetailView, DireccionCreateView, DireccionUpdateView,
    DepartamentoListView, DepartamentoDetailView, DepartamentoCreateView, DepartamentoUpdateView,
    # === Vistas de Cuadrilla - DEBEN SER AGREGADAS EN views.py ===
    CuadrillaListView, CuadrillaDetailView, CuadrillaCreateView, CuadrillaUpdateView, CuadrillaDeleteView 
    # =============================================================
)

# Definir el namespace de la aplicación
app_name = 'organizacion' 

urlpatterns = [ 
    # Modulo Dirección (CRUD completo)
    path('direcciones/', DireccionListView.as_view(), name='direccion_list'),
    path('direcciones/crear/', DireccionCreateView.as_view(), name='direccion_create'),
    path('direcciones/<int:pk>/', DireccionDetailView.as_view(), name='direccion_detail'),
    path('direcciones/<int:pk>/editar/', DireccionUpdateView.as_view(), name='direccion_update'),

    # Modulo Departamento (CRUD completo)
    path('departamentos/', DepartamentoListView.as_view(), name='departamento_list'),
    path('departamentos/crear/', DepartamentoCreateView.as_view(), name='departamento_create'),
    path('departamentos/<int:pk>/', DepartamentoDetailView.as_view(), name='departamento_detail'),
    path('departamentos/<int:pk>/editar/', DepartamentoUpdateView.as_view(), name='departamento_update'),

    # --- Modulo Cuadrilla (CRUD completo)
    path('cuadrillas/', CuadrillaListView.as_view(), name='cuadrilla_list'),
    path('cuadrillas/crear/<int:departamento_pk>/', CuadrillaCreateView.as_view(), name='cuadrilla_create'), 
    path('cuadrillas/<int:pk>/', CuadrillaDetailView.as_view(), name='cuadrilla_detail'),
    path('cuadrillas/<int:pk>/editar/', CuadrillaUpdateView.as_view(), name='cuadrilla_update'),
    path('cuadrillas/<int:pk>/eliminar/', CuadrillaDeleteView.as_view(), name='cuadrilla_delete'),
]