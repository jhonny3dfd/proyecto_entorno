from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView 
from django.db import transaction
from django.contrib import messages 
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest

from .models import Solicitud, Resolucion, Encuesta, Multimedia # <-- ¡IMPORTAR MULTIMEDIA!
from .forms import SolicitudForm, EncuestaForm, ResolucionForm
from usuarios.models import Usuario

# --- FUNCIÓN AUXILIAR PARA OBTENER EL MODELO Usuario CUSTOM ---
def _get_custom_user(request):
    """Obtiene una instancia de tu modelo Usuario, asumiendo que coincide con el user de Django."""
    if not request.user.is_authenticated:
        return None
    try:
        return Usuario.objects.get(pk=request.user.pk)
    except Usuario.DoesNotExist:
        return Usuario.objects.first() 
    except Exception:
        return None

# --- 1. VISTA DE LISTADO ---
class SolicitudListView(ListView):
    model = Solicitud
    template_name = 'incidencias/solicitud_list.html'
    context_object_name = 'solicitudes'
    queryset = Solicitud.objects.select_related('cuadrilla').all()
    
# --- 2. VISTA DE DETALLE ---
class SolicitudDetailView(DetailView):
    model = Solicitud
    template_name = 'incidencias/solicitud_detail.html'
    context_object_name = 'solicitud'
    # Cargamos Cuadrilla, Encuesta, Resolución y la Multimedia de la Encuesta
    queryset = Solicitud.objects.select_related('cuadrilla').prefetch_related(
        'encuesta_set', 
        'resolucion_set',
        'encuesta_set__multimedia_set' # <-- Pre-cargar Multimedia
    ).all()

# --- 3. VISTA DE CREACIÓN (Maneja Solicitud, Encuesta y Multimedia) ---
class SolicitudCreateView(CreateView):
    model = Solicitud
    template_name = 'incidencias/solicitud_form.html' 
    form_class = SolicitudForm 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # Pasa self.request.FILES para que EncuestaForm pueda validar el archivo
            context['encuesta_form'] = EncuestaForm(self.request.POST, self.request.FILES) 
        else:
            context['encuesta_form'] = EncuestaForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        encuesta_form = context['encuesta_form']
        
        # Validar ambos formularios, incluyendo el campo de archivo en EncuestaForm
        if encuesta_form.is_valid():
            with transaction.atomic():
                # 1. Guardar Solicitud
                solicitud = form.save(commit=False)
                solicitud.estado = 'CREADA' 
                solicitud.save()
                
                # 2. Guardar Encuesta
                encuesta = encuesta_form.save(commit=False)
                encuesta.solicitud = solicitud
                encuesta.usuario = _get_custom_user(self.request) 
                encuesta.save()

                # 3. Lógica de Multimedia: Procesar el archivo adjunto
                archivo = encuesta_form.cleaned_data.get('archivo_adjunto')
                if archivo:
                    # Determinar el tipo (simple: imagen/video/otro)
                    mime_type = archivo.content_type.split('/')[0] if archivo.content_type else 'otro'
                    
                    # Crear la instancia de Multimedia
                    Multimedia.objects.create(
                        encuesta=encuesta,
                        tipo_multimedia=mime_type, 
                        ruta=archivo
                    )
                    messages.info(self.request, f'Archivo adjunto ({mime_type}) guardado.')
                # -----------------------------------------------------------

            messages.success(self.request, 'La Solicitud e Incidencia fueron creadas exitosamente.')
            return redirect(solicitud.get_absolute_url())
        else:
            # Si la encuesta falla, muestra ambos formularios con errores
            messages.error(self.request, 'Error en los datos de la Incidencia.')
            return self.form_invalid(form)

# --- 4. VISTA DE EDICIÓN (Maneja Solicitud, Encuesta y Multimedia) ---
class SolicitudUpdateView(UpdateView): 
    model = Solicitud
    form_class = SolicitudForm 
    template_name = 'incidencias/solicitud_form.html' 

    def get_object(self, queryset=None):
        return get_object_or_404(Solicitud, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitud = self.get_object()
        
        encuesta_instance = get_object_or_404(Encuesta, solicitud=solicitud)
        
        if self.request.POST:
            # Pasa self.request.FILES para que EncuestaForm pueda validar el archivo
            context['encuesta_form'] = EncuestaForm(self.request.POST, self.request.FILES, instance=encuesta_instance)
        else:
            context['encuesta_form'] = EncuestaForm(instance=encuesta_instance)

        # También pasamos la multimedia existente para mostrarla en el template
        context['multimedia_existente'] = Multimedia.objects.filter(encuesta=encuesta_instance)
            
        return context

    def form_valid(self, form):
        """Procesa y guarda ambos formularios."""
        context = self.get_context_data()
        encuesta_form = context['encuesta_form']
        
        if encuesta_form.is_valid():
            with transaction.atomic():
                # 1. Guardar Solicitud
                self.object = form.save() 
                
                # 2. Guardar Encuesta
                encuesta = encuesta_form.save() 

                # 3. Lógica de Multimedia: Procesar el NUEVO archivo adjunto
                archivo = encuesta_form.cleaned_data.get('archivo_adjunto')
                if archivo:
                    mime_type = archivo.content_type.split('/')[0] if archivo.content_type else 'otro'
                    
                    # Crea una NUEVA instancia de Multimedia. Esto permite adjuntar más archivos 
                    # sin borrar los anteriores, que es el comportamiento más seguro.
                    Multimedia.objects.create(
                        encuesta=encuesta,
                        tipo_multimedia=mime_type, 
                        ruta=archivo
                    )
                    messages.info(self.request, f'Nuevo archivo adjunto ({mime_type}) guardado.')
            
            messages.success(self.request, 'La Solicitud e Incidencia fueron actualizadas exitosamente.')
            return redirect(self.object.get_absolute_url())
        else:
            messages.error(self.request, 'Hubo un error al actualizar la información de la Incidencia.')
            return self.form_invalid(form)
            
    def get_success_url(self):
        return reverse_lazy('solicitud_detail', kwargs={'pk': self.object.pk})

# --- 5. VISTA DE RESOLUCIÓN ---
class ResolucionCreateView(CreateView):
    # ... (El resto de la vista ResolucionCreateView no cambia) ...
    model = Resolucion
    form_class = ResolucionForm
    template_name = 'incidencias/resolucion_form.html' 

    def get_success_url(self):
        return reverse_lazy('solicitud_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solicitud'] = get_object_or_404(Solicitud, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        # 1. Obtener la Solicitud
        solicitud = get_object_or_404(Solicitud, pk=self.kwargs['pk'])
        
        # 2. Guardar la Resolución, sin hacer commit
        resolucion = form.save(commit=False)
        
        # 3. Asignar la Solicitud y el Usuario Resolutor
        resolucion.solicitud = solicitud
        resolucion.usuario = _get_custom_user(self.request) 

        resolucion.save() # Guardar la Resolución

        # 4. Cambiar el estado de la Solicitud a FINALIZADA
        if solicitud.estado != 'FINALIZADA':
            solicitud.estado = 'FINALIZADA'
            solicitud.save()
            messages.success(self.request, 'Resolución registrada y Solicitud marcada como Finalizada.')
        else:
            messages.info(self.request, 'Resolución registrada. La Solicitud ya estaba Finalizada.')

        return super().form_valid(form) 


# --- 6. FUNCIÓN PARA TOGGLE DE ESTADO DE ENCUESTA ---
@require_POST
def toggle_encuesta_status(request, pk):
    # ... (La lógica de esta función auxiliar no cambia) ...
    solicitud = get_object_or_404(Solicitud, pk=pk)
    try:
        Encuesta.objects.get(solicitud=solicitud)
    except Encuesta.DoesNotExist:
        return HttpResponseBadRequest("La Solicitud no tiene una Encuesta asociada.")

    return JsonResponse({
        'status': 'success', 
        'message': f'Acción de estado simulada para la Encuesta de Solicitud #{pk}.'
    })