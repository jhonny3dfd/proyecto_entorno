from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Direccion, Departamento, Cuadrilla


class DireccionListView(ListView):
    """Muestra un listado de todas las Direcciones."""
    model = Direccion
    template_name = 'organizacion/direccion_list.html'
    context_object_name = 'direcciones'
    
class DireccionDetailView(DetailView):
    """Muestra el detalle de una Dirección específica."""
    model = Direccion
    template_name = 'organizacion/direccion_detail.html'
    context_object_name = 'direccion'


class DepartamentoDetailView(DetailView):
    """Muestra el detalle de un Departamento específico."""
    model = Departamento
    template_name = 'organizacion/departamento_detail.html'
    context_object_name = 'departamento'