from django.contrib import admin
from .models import Solicitud, Encuesta, Resolucion, Multimedia

class EncuestaAdmin(admin.ModelAdmin):
    # Campos que quiere mostrar en el formulario de edición/creación
    fields = (
        'solicitud', 'usuario', 'titulo', 'descripcion', 
        'ubicacion', 'prioridad', 'nombre_vecino', 
        'telefono_vecino', 'correo_vecino'
    )
    
    # NUEVA LÍNEA: Usa raw_id_fields para los ForeignKeys
    # El usuario y la solicitud se seleccionarán introduciendo su ID.
    raw_id_fields = ('solicitud', 'usuario',) # <--- ¡Agregar esta línea!
    
    # Esta función se llama al inicio del formulario para dar valores iniciales
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        solicitud_id = request.GET.get('solicitud')
        
        if solicitud_id:
            initial['solicitud'] = solicitud_id
            
        return initial

# Registra los modelos principales
admin.site.register(Solicitud)
admin.site.register(Encuesta, EncuestaAdmin) 
admin.site.register(Resolucion)
admin.site.register(Multimedia)