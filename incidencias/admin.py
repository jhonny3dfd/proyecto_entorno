from django.contrib import admin

# incidencias/admin.py

from django.contrib import admin
from .models import Solicitud, Encuesta, Resolucion, Multimedia # Asegúrate de importar todos

# Registra los modelos principales
admin.site.register(Solicitud)
admin.site.register(Encuesta)
admin.site.register(Resolucion)
admin.site.register(Multimedia)