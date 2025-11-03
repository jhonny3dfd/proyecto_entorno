
from django.urls import path, include
from .views import Crear_Usuarios, Lista_Usuarios, Menu_Usuarios, usuario_bloquear, usuario_eliminar, usuario_editar

from core.urls import core_urlpatterns

usuarios_urlpatterns = [
    path('', include(core_urlpatterns)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),
    
    path('usuarios/', Menu_Usuarios, name='menu_usuarios'),  
    path('usuarios/crear/', Crear_Usuarios, name='crear_usuarios'),
    path('usuarios/lista/', Lista_Usuarios, name='lista_usuarios'),  
    path('usuarios/bloquear/<int:id_usuario>', usuario_bloquear, name='bloquear_usuarios'),
    path('usuarios/eliminar/<int:id_usuario>', usuario_eliminar, name='eliminar_usuarios'),
    path('usuarios/editar/<int:id_usuario>', usuario_editar, name='editar_usuarios'),
    ]

