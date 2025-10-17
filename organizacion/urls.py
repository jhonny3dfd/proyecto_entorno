# organizacion/urls.py

from django.urls import path
from .views import (
    DireccionListView, DireccionDetailView, DireccionCreateView, DireccionUpdateView, DireccionDeleteView,
    DepartamentoListView, DepartamentoDetailView, DepartamentoCreateView, DepartamentoUpdateView, DepartamentoDeleteView
)

# Definir el namespace de la aplicación
app_name = 'organizacion' 

# ¡CORRECCIÓN CLAVE! Cambiar organizacion_urlpatterns a urlpatterns
urlpatterns = [ 
    # Módulo Dirección (CRUD completo)
    path('direcciones/', DireccionListView.as_view(), name='direccion_list'),
    path('direcciones/crear/', DireccionCreateView.as_view(), name='direccion_create'),
    path('direcciones/<int:pk>/', DireccionDetailView.as_view(), name='direccion_detail'),
    path('direcciones/<int:pk>/editar/', DireccionUpdateView.as_view(), name='direccion_update'),
    path('direcciones/<int:pk>/eliminar/', DireccionDeleteView.as_view(), name='direccion_delete'),

    # Módulo Departamento (CRUD completo)
    path('departamentos/', DepartamentoListView.as_view(), name='departamento_list'),
    path('departamentos/crear/', DepartamentoCreateView.as_view(), name='departamento_create'),
    path('departamentos/<int:pk>/', DepartamentoDetailView.as_view(), name='departamento_detail'),
    path('departamentos/<int:pk>/editar/', DepartamentoUpdateView.as_view(), name='departamento_update'),
    path('departamentos/<int:pk>/eliminar/', DepartamentoDeleteView.as_view(), name='departamento_delete'),
]