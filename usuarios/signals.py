from django.db.models.signals import post_migrate
from django.dispatch import receiver

Roles = [
    'Administrador', #o SECPLA, pero digamosle admin
    'Direccion',
    'Departamento',
    'Territorial',
    'Cuadrilla'  
]

@receiver(post_migrate)
def crear_roles(sender,**kwargs):
        # Según entiendo, despues de migrar se ejecuta
        # esta función y lo que hace es añadir los roles a la tabla

        if sender.label =='usuarios':
            from usuarios.models import Rol

            for nombre_rol in Roles:
                Rol.objects.get_or_create(nombre_rol=nombre_rol)
            print("Roles creados")