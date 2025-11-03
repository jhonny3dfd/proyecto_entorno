from django.db import models

class Direccion(models.Model):
    nombre_encargado = models.CharField(max_length=200)
    correo_encargado = models.EmailField()
    nombre_direccion = models.CharField(max_length=255)
    activa = models.BooleanField(default=True, verbose_name="Dirección Activa") 

    def __str__(self):
        return self.nombre_direccion
class Departamento(models.Model):
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    nombre_encargado = models.CharField(max_length=200)
    correo_encargado = models.EmailField()
    departamento = models.CharField(max_length=200, verbose_name="Departamento") 
    activo = models.BooleanField(default=True, verbose_name="Departamento Activo")

    def __str__(self):
        return self.departamento
    
class Cuadrilla(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    nombre_cuadrilla = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_cuadrilla

class UsuarioCuadrilla(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    cuadrilla = models.ForeignKey(Cuadrilla, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'cuadrilla')

    def __str__(self):
        return f'{self.usuario} asignado a {self.cuadrilla}'

class EncargadoDepartamento(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.usuario} es encargado de {self.departamento}'

class EncargadoDireccion(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.usuario} es encargado de {self.direccion}'