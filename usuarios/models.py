from django.db import models

# NOTA: En un proyecto real, considera usar django.contrib.auth.models.User o AbstractUser.

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
    contraseña = models.CharField(max_length=128) # Almacenará el hash de la contraseña

    def __str__(self):
        return f'{self.nombre} {self.apellido}'