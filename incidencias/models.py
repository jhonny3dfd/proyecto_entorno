from django.db import models
from django.utils import timezone
from django.urls import reverse

ESTADO_CHOICES = [
    ('CREADA', 'Creada'),
    ('ABIERTA', 'Abierta'),
    ('EN PROCESO', 'En Proceso'),
    ('FINALIZADA', 'Finalizada'),
    ('RECHAZADA', 'Rechazada'),
]
PRIORIDAD_CHOICES = [
    ('ALTA', 'Alta'),
    ('MEDIA', 'Media'),
    ('BAJA', 'Baja'),
]


from django.db import models
from django.utils import timezone

class Solicitud(models.Model):
    cuadrilla = models.ForeignKey('organizacion.Cuadrilla', on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True)
    tipo_incidencia = models.CharField(max_length=100)

    def get_absolute_url(self):
        """Define la URL de detalle después de la creación exitosa."""
        return reverse('solicitud_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Solicitud #{self.id} - {self.tipo_incidencia}"

class Encuesta(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE) 
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=255)
    prioridad = models.CharField(max_length=50, choices=PRIORIDAD_CHOICES)
    nombre_vecino = models.CharField(max_length=200)
    telefono_vecino = models.CharField(max_length=20)
    correo_vecino = models.EmailField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Detalles para Solicitud #{self.solicitud.id}"

class Resolucion(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    cuadrilla = models.ForeignKey(
        'organizacion.Cuadrilla',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    descripcion = models.TextField()
    fecha_resolucion = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"Resolución para Solicitud #{self.solicitud.id}"

class Multimedia(models.Model):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    tipo_multimedia = models.CharField(max_length=50)
    ruta = models.FileField(upload_to='multimedia_incidencias/')

    def __str__(self):
        return f"{self.tipo_multimedia} para Solicitud #{self.solicitud.id}"

class Pregunta(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    pregunta = models.CharField(max_length=500)

    def __str__(self):
        return self.pregunta

class Respuesta(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    respuesta = models.TextField()

    def __str__(self):
        return f"Respuesta para Solicitud #{self.solicitud.id}"
    
class UsuarioTerritorial(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    departamento = models.ForeignKey('organizacion.Departamento', on_delete=models.CASCADE)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('solicitud', 'departamento', 'usuario')

    def __str__(self):
        return f"{self.usuario} asignado a {self.solicitud} en {self.departamento}"