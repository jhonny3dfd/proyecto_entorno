"""
URL configuration for proyecto_entorno project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path, include # pyright: ignore[reportMissingModuleSource]
from core.urls import core_urlpatterns
from usuarios.urls import usuarios_urlpatterns
from incidencias.urls import incidencias_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('organizacion/', include('organizacion.urls')),
    path('', include(usuarios_urlpatterns)),
    path('',include(incidencias_urlpatterns)),
    path('',include(core_urlpatterns)),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/',include('registration.urls')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # 1. Archivos Estáticos (CSS, JS, imágenes de diseño, etc.)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # 2. Archivos Media (Imágenes subidas por el usuario, como la foto de fondo)
    # ¡Asegúrate de que STATIC_URL, MEDIA_ROOT y MEDIA_URL estén definidos en settings.py!
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)