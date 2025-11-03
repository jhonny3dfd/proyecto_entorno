# incidencias/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model 
from .models import Solicitud, Encuesta, Resolucion, Multimedia


class EncuestaAdmin(admin.ModelAdmin):
    fields = (
        'solicitud', 'usuario', 'titulo', 'descripcion', 
        'ubicacion', 'prioridad', 'nombre_vecino', 
        'telefono_vecino', 'correo_vecino'
    )
    
    raw_id_fields = ('solicitud', 'usuario',) 
    

admin.site.register(Solicitud)
admin.site.register(Encuesta, EncuestaAdmin) 
admin.site.register(Resolucion)
admin.site.register(Multimedia)

