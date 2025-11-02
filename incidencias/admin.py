# incidencias/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model # ✅ Importar de forma segura
from .models import Solicitud, Encuesta, Resolucion, Multimedia

# Opcional: Definir el modelo de Usuario (solo si se necesita explícitamente más adelante)
# User = get_user_model() 

class EncuestaAdmin(admin.ModelAdmin):
    # Campos que quiere mostrar en el formulario de edición/creación
    fields = (
        'solicitud', 'usuario', 'titulo', 'descripcion', 
        'ubicacion', 'prioridad', 'nombre_vecino', 
        'telefono_vecino', 'correo_vecino'
    )
    
    # Usar raw_id_fields para el usuario. Django usa el string de referencia aquí.
    raw_id_fields = ('solicitud', 'usuario',) 
    
    # ... el resto de la lógica de tu EncuestaAdmin ...

# Registra los modelos principales
admin.site.register(Solicitud)
admin.site.register(Encuesta, EncuestaAdmin) 
admin.site.register(Resolucion)
admin.site.register(Multimedia)

# Si tenías otros modelos registrados, añádelos aquí.
# admin.site.register(UsuarioTerritorial) # Ejemplo de tu models.py