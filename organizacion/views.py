# organizacion/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy 
from .models import Direccion, Departamento, Cuadrilla
from django.shortcuts import redirect 
from django.urls import reverse


# --- Vistas de Direccion (CRUD) ---

class DireccionListView(ListView):
    model = Direccion 
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        action = request.GET.get('action')
        
        if action in ['bloquear', 'activar']:
            if action == 'bloquear':
                self.object.activa = False
            elif action == 'activar':
                self.object.activa = True
                
            self.object.save()
            
            return redirect(self.get_success_url())
            
        # Si no es una accion especial, ejecutar el POST normal (edicion de formulario)
        return super().post(request, *args, **kwargs)

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
    fields = ['direccion', 'nombre_encargado', 'correo_encargado', 'departamento', 'activo'] 
    template_name = 'organizacion/departamento_form.html' 
    success_url = reverse_lazy('organizacion:departamento_list')
    
    def get_initial(self):
        initial = super().get_initial()
        direccion_id = self.request.GET.get('direccion_id')
        if direccion_id:
            try:
                initial['direccion'] = Direccion.objects.get(pk=direccion_id)
            except Direccion.DoesNotExist:
                pass
        return initial

class DepartamentoUpdateView(UpdateView):
    model = Departamento
    fields = ['direccion', 'nombre_encargado', 'correo_encargado', 'departamento', 'activo']
    template_name = 'organizacion/departamento_form.html'
    success_url = reverse_lazy('organizacion:departamento_list')

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



#Vista de Cuadrillas

class CuadrillaListView(ListView):
    model = Cuadrilla
    template_name = 'organizacion/cuadrilla_list.html' 
    context_object_name = 'cuadrillas'

class CuadrillaDetailView(DetailView):
    model = Cuadrilla
    template_name = 'organizacion/cuadrilla_detail.html' 
    context_object_name = 'cuadrilla'

class CuadrillaCreateView(CreateView):
    model = Cuadrilla
    fields = ['departamento', 'nombre_cuadrilla'] 
    template_name = 'organizacion/cuadrilla_form.html' 

    # 1. Obtiene el 'departamento_pk' de la URL y lo usa como valor inicial del campo 'departamento'
    def get_initial(self):
        initial = super().get_initial()
        departamento_pk = self.kwargs.get('departamento_pk')
        if departamento_pk:
            initial['departamento'] = departamento_pk
        return initial

    # 2. Redirecciona al detalle del Departamento (no al listado de cuadrillas)
    def get_success_url(self):
        departamento_pk = self.kwargs.get('departamento_pk')
        if departamento_pk:
            return reverse('organizacion:departamento_detail', kwargs={'pk': departamento_pk})
        return reverse_lazy('organizacion:departamento_list') 
class CuadrillaUpdateView(UpdateView):
    model = Cuadrilla
    fields = ['departamento', 'nombre_cuadrilla'] 
    template_name = 'organizacion/cuadrilla_form.html'
    success_url = reverse_lazy('organizacion:cuadrilla_list')

class CuadrillaDeleteView(DeleteView):
    model = Cuadrilla
    template_name = 'organizacion/cuadrilla_confirm_delete.html' 
    success_url = reverse_lazy('organizacion:cuadrilla_list')