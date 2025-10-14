from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView # <--- Importar CreateView
from .models import Solicitud
from .forms import SolicitudForm
class SolicitudListView(ListView):
    model = Solicitud
    template_name = 'incidencias/solicitud_list.html'
    context_object_name = 'solicitudes'
    # Solo necesitamos cuadrilla para la lista, y es select_related
    queryset = Solicitud.objects.select_related('cuadrilla').all()
    
class SolicitudDetailView(DetailView):
    model = Solicitud
    template_name = 'incidencias/solicitud_detail.html'
    context_object_name = 'solicitud'
    # Cargamos cuadrilla y pre-cargamos la encuesta para la eficiencia
    # Nota: El nombre 'encuesta_set' es la relación inversa por defecto
    queryset = Solicitud.objects.select_related('cuadrilla').prefetch_related('encuesta_set').all()

class SolicitudCreateView(CreateView):
    model = Solicitud
    # Nombre de la plantilla para el formulario (debes crear este archivo)
    template_name = 'incidencias/solicitud_form.html' 
    # Usaremos todos los campos por simplicidad, puedes cambiarlos a ['campo1', 'campo2', ...]
    fields = ['cuadrilla', 'estado', 'observaciones', 'tipo_incidencia'] 
    success_url = reverse_lazy('solicitud_list')

class SolicitudCreateView(CreateView):
    model = Solicitud
    form_class = SolicitudForm # Usamos el formulario que creamos
    template_name = 'incidencias/solicitud_form.html' # El template que crearemos
    success_url = reverse_lazy('solicitud_list') # Redirigir al listado después de crear