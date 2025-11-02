# organizacion/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy 
from .models import Direccion, Departamento, Cuadrilla
from django.shortcuts import redirect # Importar redirect


# --- Vistas de Dirección (CRUD) ---

class DireccionListView(ListView):
    """Muestra un listado de todas las Direcciones."""
    model = Direccion # <--- DEBE SER EL MODELO CORRECTO
    template_name = 'organizacion/direccion_list.html'
    context_object_name = 'direcciones'
    
class DireccionDetailView(DetailView):
    model = Direccion
    template_name = 'organizacion/direccion_detail.html'
    context_object_name = 'direccion'

class DireccionCreateView(CreateView):
    model = Direccion
    fields = ['nombre_encargado', 'correo_encargado', 'nombre_direccion', 'activa'] 
    template_name = 'organizacion/direccion_form.html' 
    success_url = reverse_lazy('organizacion:direccion_list')

class DireccionUpdateView(UpdateView):
    model = Direccion
    fields = ['nombre_encargado', 'correo_encargado', 'nombre_direccion', 'activa']
    template_name = 'organizacion/direccion_form.html'
    success_url = reverse_lazy('organizacion:direccion_list')

    # *** Lógica para manejar Bloquear/Activar ***
    def post(self, request, *args, **kwargs):
        # 1. Obtener el objeto actual (Dirección)
        self.object = self.get_object() 
        
        # 2. Verificar si viene la acción 'action' en la URL (Query Parameter)
        action = request.GET.get('action')
        
        if action in ['bloquear', 'activar']:
            # Lógica de bloqueo/activación
            if action == 'bloquear':
                self.object.activa = False
            elif action == 'activar':
                self.object.activa = True
                
            self.object.save()
            
            # Redirigir al listado
            return redirect(self.get_success_url())
            
        # 3. Si no es una acción especial, ejecutar el POST normal (edición de formulario)
        return super().post(request, *args, **kwargs)

class DireccionDeleteView(DeleteView):
    # Usaremos DeleteView para confirmar la "desactivación"
    model = Direccion
    template_name = 'organizacion/direccion_confirm_delete.html' 
    success_url = reverse_lazy('organizacion:direccion_list')


# --- Vistas de Departamento (CRUD) ---

class DepartamentoListView(ListView):
    model = Departamento
    template_name = 'organizacion/departamento_list.html'
    context_object_name = 'departamentos'

class DepartamentoDetailView(DetailView):
    model = Departamento
    template_name = 'organizacion/departamento_detail.html'
    context_object_name = 'departamento'

class DepartamentoCreateView(CreateView):
    model = Departamento
    # Incluimos 'direccion' para que aparezca en el formulario
    fields = ['direccion', 'nombre_encargado', 'correo_encargado', 'departamento', 'activo'] 
    template_name = 'organizacion/departamento_form.html' 
    success_url = reverse_lazy('organizacion:departamento_list')
    
    # Nuevo: Permite preseleccionar la Dirección si viene en la URL
    def get_initial(self):
        initial = super().get_initial()
        direccion_id = self.request.GET.get('direccion_id')
        if direccion_id:
            try:
                # Esto selecciona la Dirección en el campo 'direccion' del formulario
                initial['direccion'] = Direccion.objects.get(pk=direccion_id)
            except Direccion.DoesNotExist:
                pass
        return initial

class DepartamentoUpdateView(UpdateView):
    model = Departamento
    fields = ['direccion', 'nombre_encargado', 'correo_encargado', 'departamento', 'activo']
    template_name = 'organizacion/departamento_form.html'
    success_url = reverse_lazy('organizacion:departamento_list')

    # Lógica para manejar Bloquear/Activar
    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        action = request.GET.get('action')
        
        if action in ['bloquear', 'activar']:
            if action == 'bloquear':
                self.object.activo = False
            elif action == 'activar':
                self.object.activo = True
            
            self.object.save()
            return redirect(self.get_success_url())
            
        return super().post(request, *args, **kwargs)

class DepartamentoDeleteView(DeleteView):
    model = Departamento
    template_name = 'organizacion/departamento_confirm_delete.html' 
    success_url = reverse_lazy('organizacion:departamento_list')