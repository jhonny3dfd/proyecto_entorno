from django.contrib import admin
from .models import Usuario, Rol # Importa tus modelos

# 1. Registra el modelo Usuario para que aparezca en el panel.
admin.site.register(Usuario)

admin.site.register(Rol)