from django.db import models


class Rol(models.Model):
    nombre_rol = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    contraseña = models.CharField(max_length=128) 
    esta_activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'