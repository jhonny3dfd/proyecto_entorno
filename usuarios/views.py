from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from registration.models import Profile
from .models import Usuario, Rol
from .forms import *
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, redirect
from .models import Usuario

# MENÚ PRINCIPAL DE USUARIOS
@login_required
def Menu_Usuarios(request):
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Hubo un error')
        return redirect('login')
    
    if profile.group_id == 1:
        return render(request, 'usuarios/Menu_Usuarios.html')
    else:
        return redirect('logout')

# CREAR USUARIO
@login_required
def Crear_Usuarios(request):
    roles = Rol.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        contraseña = request.POST.get('contraseña')
        rol_id = request.POST.get('rol') 
        hashed_password = make_password(contraseña)

        try:
            rol_obj = Rol.objects.get(id=rol_id)
        except Rol.DoesNotExist:
            return render(request, 'usuarios/Crear_Usuarios.html', {
                'roles': roles,
                'error_message': 'El rol seleccionado no es válido.'
            })

        Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            telefono=telefono,
            contraseña=hashed_password,  
            rol=rol_obj,
            esta_activo=True
        )

        return redirect('lista_usuarios') 

    return render(request, 'usuarios/Crear_Usuarios.html', {
        'roles': roles
    })

# LISTA DE USUARIOS
@login_required
def Lista_Usuarios(request):
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Hubo un error')
        return redirect('login')
    
    if profile.group_id == 1:
        usuarios = Usuario.objects.all()
        return render(request, 'usuarios/Lista_Usuarios.html', {'usuarios': usuarios})
    else:
        return redirect('logout')

@login_required
def usuario_editar(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    if request.method == 'POST':
        form = UsuarioForm(request.POST,instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    template_name= 'usuarios/usuario_editar.html'
    return render(request, template_name, {'form':form})

@login_required
def usuario_eliminar(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    if request.method == 'POST':
        usuario.delete()
        return redirect('menu_usuarios')
    return redirect

@login_required
def usuario_bloquear_desbloquear(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)

    # Invertir el estado (si está activo, lo desactiva, y viceversa)
    usuario.esta_activo = not usuario.esta_activo
    usuario.save()

    # Redirigir de nuevo a la lista
    return redirect('lista_usuarios')