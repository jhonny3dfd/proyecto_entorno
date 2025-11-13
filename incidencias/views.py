from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView 
from django.db import transaction
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SolicitudForm, EncuestaForm, ResolucionForm, SolicitudDerivarForm

from .models import Solicitud, Resolucion, Encuesta , Multimedia
from .forms import SolicitudForm, EncuestaForm, ResolucionForm
from usuarios.models import Usuario 

# --- 1. FUNCIÓN AUXILIAR PARA OBTENER EL PERFIL DE USUARIO ---
def _get_custom_user(request):
    if not request.user.is_authenticated:
        return None
    
    try:
        return Usuario.objects.get(correo=request.user.email) 
        
    except Usuario.DoesNotExist:
        messages.error(request, f"ERROR: El usuario {request.user.email} (Admin) no tiene un perfil en la tabla 'usuarios.Usuario'. Debe crearlo.")
        # 🚨 ESTO DEBE CAMBIAR DEBAJO 🚨
        return None # <-- Debe retornar None para evitar el bucle infinito y la falla
        
    except Exception as e:
        messages.error(request, f"Error inesperado al obtener el perfil de usuario: {e}")
        return None

# --- 2. VISTAS BASADAS EN CLASES ---

class SolicitudListView(LoginRequiredMixin, ListView):
    model = Solicitud
    context_object_name = 'solicitudes'
    template_name = 'incidencias/solicitud_list.html'
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        filtro_estado = self.request.GET.get('estado')

        if filtro_estado:
            if filtro_estado == 'ENCUESTA_ACTIVA':
                # Filtra Solicitudes cuya Encuesta está activa
                queryset = queryset.filter(encuesta__activa=True)
                
            elif filtro_estado == 'ENCUESTA_BLOQUEADA':
                # Filtra Solicitudes cuya Encuesta NO está activa
                queryset = queryset.filter(encuesta__activa=False)
            
            else:
                # Filtra por estados de Solicitud (CREADA, FINALIZADA, ABIERTA, etc.)
                # El valor de filtro_estado debe coincidir exactamente con el valor del modelo
                queryset = queryset.filter(estado=filtro_estado)

        return queryset

class SolicitudDetailView(LoginRequiredMixin, DetailView):
    model = Solicitud
    context_object_name = 'solicitud'
    template_name = 'incidencias/solicitud_detail.html'


class SolicitudCreateView(LoginRequiredMixin, CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'incidencias/solicitud_form.html'
    success_url = reverse_lazy('solicitud_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['encuesta_form'] = EncuestaForm(self.request.POST, self.request.FILES)
        else:
            context['encuesta_form'] = EncuestaForm() # Primera carga
            
        return context

    def form_valid(self, form):
        custom_user = _get_custom_user(self.request)
        
        if custom_user is None:
             return self.form_invalid(form) 

        context = self.get_context_data()
        encuesta_form = context['encuesta_form']
        
        if not encuesta_form.is_valid():
             return self.render_to_response(self.get_context_data(form=form))


        with transaction.atomic():
            # A. Guardar Solicitud
            solicitud = form.save(commit=False)
            solicitud.estado = 'CREADA'
            solicitud.save()

            # B. Guardar Encuesta
            encuesta = encuesta_form.save(commit=False)
            encuesta.solicitud = solicitud 
            encuesta.usuario = custom_user  
            encuesta.save()

            # C. Guardar Multimedia (si hay archivo)
            archivo = encuesta_form.cleaned_data.get('archivo_adjunto')
            if archivo:
                tipo = 'IMAGEN' if archivo.content_type.startswith('image') else 'OTRO'
                Multimedia.objects.create(
                    encuesta=encuesta,
                    tipo_multimedia=tipo,
                    ruta=archivo 
                )

        messages.success(self.request, "Solicitud y Encuesta creadas exitosamente.")
        return redirect(solicitud.get_absolute_url())

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


# --- 5. RESOLUCION CREATE VIEW --- (Lógica de tu código original, no modificada)

class ResolucionCreateView(LoginRequiredMixin, CreateView):
    model = Resolucion
    form_class = ResolucionForm
    template_name = 'incidencias/resolucion_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitud_pk = self.kwargs['pk']
        context['solicitud'] = get_object_or_404(Solicitud, pk=solicitud_pk)
        return context

    def form_valid(self, form):
        solicitud_pk = self.kwargs['pk']
        solicitud = get_object_or_404(Solicitud, pk=solicitud_pk)

        resolucion = form.save(commit=False)
        resolucion.solicitud = solicitud
        
        try:
            usuario_resolutor = Usuario.objects.first() 
        except Usuario.DoesNotExist: 
            usuario_resolutor = None

        if usuario_resolutor:
            resolucion.usuario = usuario_resolutor

        resolucion.save() 

        solicitud.estado = 'FINALIZADA'
        solicitud.save()

        messages.success(self.request, "La resolución ha sido creada y la Solicitud se ha marcado como FINALIZADA.")
        
        return redirect(solicitud.get_absolute_url())

# --- 6. SOLICITUD UPDATE VIEW --- (Asumiendo que existe en tu app)

class SolicitudUpdateView(LoginRequiredMixin, UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'incidencias/solicitud_form.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Solicitud, pk=self.kwargs['pk'])

    # 🚨 NUEVA FUNCIÓN PARA BLOQUEAR LA EDICIÓN
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # 1. Obtener la encuesta asociada
        try:
            encuesta = Encuesta.objects.get(solicitud=self.object)
        except Encuesta.DoesNotExist:
            # Si no hay encuesta, puede seguir para crearla o manejar el error.
            return super().get(request, *args, **kwargs)

        # 2. Verificar si la encuesta está activa
        if encuesta.activa:
            messages.warning(request, "La Incidencia no puede ser editada mientras la Encuesta asociada esté ACTIVA. Bloquéela primero.")
            # 3. Redirigir al detalle de la solicitud para que el usuario pueda desactivarla
            return redirect('solicitud_detail', pk=self.object.pk) 
        
        # Si la encuesta está inactiva, permite la edición
        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        # ... (El resto de tu lógica para cargar los formularios en el contexto) ...
        context = super().get_context_data(**kwargs)
        solicitud = self.get_object()
        
        try:
            encuesta_instance = Encuesta.objects.get(solicitud=solicitud)
        except Encuesta.DoesNotExist:
            encuesta_instance = None

        if self.request.POST:
            context['encuesta_form'] = EncuestaForm(self.request.POST, self.request.FILES, instance=encuesta_instance)
        else:
            context['encuesta_form'] = EncuestaForm(instance=encuesta_instance)
        
        return context

    # ... (El resto de form_valid y form_invalid de SolicitudUpdateView) ...
    def form_valid(self, form):
        # ... (Asegúrate que tu form_valid maneje la actualización de ambos formularios)
        
        context = self.get_context_data()
        encuesta_form = context['encuesta_form']
        
        if encuesta_form.is_valid():
            with transaction.atomic():
                # Guarda la Solicitud
                form.save()
                
                # Guarda la Encuesta
                encuesta = encuesta_form.save(commit=False)
                encuesta.solicitud = form.instance # Relacionar con la solicitud existente
                # El campo 'usuario' no se actualiza a menos que se necesite
                encuesta.save()

            messages.success(self.request, "Solicitud y Encuesta actualizadas exitosamente.")
            return super().form_valid(form)
        else:
            # Si la encuesta falla, re-renderiza con el error
            return self.render_to_response(self.get_context_data(form=form))


class SolicitudDerivarView(LoginRequiredMixin, UpdateView):
    """
    Permite a un usuario de Departamento asignar una Cuadrilla 
    y cambiar el estado de la Solicitud a 'DERIVADA'.
    """
    model = Solicitud
    form_class = SolicitudDerivarForm
    template_name = 'incidencias/solicitud_derivar_form.html'
    
    # Redirige al detalle después de guardar
    def get_success_url(self):
        return reverse('solicitud_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        solicitud = form.instance
        
        # Validación de estado: Solo se puede derivar si está CREADA o ABIERTA
        if solicitud.estado not in ['CREADA', 'ABIERTA']:
            messages.error(self.request, f"La Solicitud #{solicitud.pk} ya está en estado {solicitud.estado} y no puede ser derivada.")
            return self.form_invalid(form) # Retorna el formulario con el error

        # 1. Cambiar el estado a DERIVADA (es la acción principal)
        solicitud.estado = 'DERIVADA'
        
        # 2. Guarda el objeto (con la nueva cuadrilla y observaciones)
        response = super().form_valid(form)

        messages.success(self.request, f"Solicitud #{solicitud.pk} derivada a la Cuadrilla: {solicitud.cuadrilla.nombre_cuadrilla}. Estado cambiado a DERIVADA.")
        return response

    # Esto asegura que el template solicitud_derivar_form.html tenga la variable `solicitud`
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solicitud'] = self.object 
        return context


# --- 7. FUNCIÓN PARA TOGGLE DE ESTADO DE ENCUESTA --- (Lógica de tu código original, no modificada)
@require_POST
def toggle_encuesta_status(request, pk):
    """
    Alterna el estado 'activa' de la Encuesta asociada a una Solicitud.
    """
    solicitud = get_object_or_404(Solicitud, pk=pk)
    
    try:
        encuesta = Encuesta.objects.get(solicitud=solicitud)
        
        # Invertir el estado (Activa -> Inactiva / Inactiva -> Activa)
        encuesta.activa = not encuesta.activa
        encuesta.save()
        
        estado_nuevo = "ACTIVA" if encuesta.activa else "BLOQUEADA (Inactiva)"
        messages.success(request, f"El estado de la Encuesta para la Solicitud #{pk} ha cambiado a {estado_nuevo}.")
        
    except Encuesta.DoesNotExist:
        messages.error(request, f"Error: No se encontró la Encuesta asociada a la Solicitud #{pk}.")
        
    # Redirigir siempre de vuelta a la página de detalle
    return redirect('solicitud_detail', pk=pk)