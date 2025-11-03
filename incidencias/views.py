from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView 
from django.db import transaction
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Solicitud, Resolucion, Encuesta , Multimedia
from .forms import SolicitudForm, EncuestaForm, ResolucionForm
from usuarios.models import Usuario 

# --- 1. FUNCIÓN AUXILIAR PARA OBTENER EL PERFIL DE USUARIO ---
def _get_custom_user(request):
    """
    Intenta obtener el perfil de usuario personalizado (usuarios.Usuario) 
    a partir del usuario de autenticación de Django (request.user).
    """
    if not request.user.is_authenticated:
        return None
    
    try:
        return Usuario.objects.get(correo=request.user.email) 
        
    except Usuario.DoesNotExist:
        messages.error(request, f"ERROR: El usuario {request.user.email} (Admin) no tiene un perfil en la tabla 'usuarios.Usuario'. Debe crearlo.")
        return None 
    
    except Exception as e:
        messages.error(request, f"Error inesperado al obtener el perfil de usuario: {e}")
        return None


# --- 2. VISTAS BASADAS EN CLASES ---

class SolicitudListView(LoginRequiredMixin, ListView):
    model = Solicitud
    context_object_name = 'solicitudes'
    template_name = 'incidencias/solicitud_list.html'
    ordering = ['-fecha_creacion']

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

    def get_context_data(self, **kwargs):
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
        
        context['multimedia_existente'] = Multimedia.objects.filter(encuesta__solicitud=solicitud)

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Solicitud, pk=self.kwargs['pk'])

    def form_valid(self, form):
        messages.success(self.request, "Solicitud y Encuesta actualizadas exitosamente.")
        return super().form_valid(form)


# --- 7. FUNCIÓN PARA TOGGLE DE ESTADO DE ENCUESTA --- (Lógica de tu código original, no modificada)
@require_POST
def toggle_encuesta_status(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Usuario no autenticado")

    solicitud = get_object_or_404(Solicitud, pk=pk)
    try:
        encuesta = Encuesta.objects.get(solicitud=solicitud)
        encuesta.activa = not encuesta.activa
        encuesta.save()
        messages.success(request, f"El estado de la encuesta ha sido cambiado a {'Activa' if encuesta.activa else 'Inactiva'}.")
    except Encuesta.DoesNotExist:
        messages.error(request, "Error: No existe una encuesta para esta solicitud.")

    return redirect('solicitud_detail', pk=pk)