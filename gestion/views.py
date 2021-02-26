from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Rol

User = get_user_model()


# Create your views here.

###############################################################################
# Registro de Usuario
###############################################################################

from .forms import FormularioRegistroUser
def registro(request):
    if request.method == 'POST':
        form = FormularioRegistroUser(request.POST)
        if form.is_valid():
            rol = Rol.objects.get(nombre="Miembro")
            User.objects.create_user(username=form.cleaned_data.get('username'),
                                    rut=form.cleaned_data.get('rut'),
                                    first_name=form.cleaned_data.get('first_name'),
                                    apellido_paterno=form.cleaned_data.get('apellido_paterno'),
                                    apellido_materno=form.cleaned_data.get('apellido_materno'),
                                    resumen=form.cleaned_data.get('resumen'),
                                    telefono=form.cleaned_data.get('telefono'),
                                    sexo=form.cleaned_data.get('sexo'),
                                    estado_civil=form.cleaned_data.get('estado_civil'),
                                    direccion_calle=form.cleaned_data.get('direccion_calle'),
                                    direccion_numero=form.cleaned_data.get('direccion_numero'),
                                    comuna=form.cleaned_data.get('comuna'),
                                    asamblea=form.cleaned_data.get('asamblea'),
                                    password=form.cleaned_data.get('password1'), 
                                    rol=rol)
            #user = authenticate(username=username, password=raw_password, rol="subcliente")
            #login(request, user)
            list(messages.get_messages(request))
            messages.success(request, "El usuario fué creado exitósamente!")
            return redirect('asambleas:principal')
    else:
        form = FormularioRegistroUser()
    return render(request, 'gestion/usuario_registro.html', {'form': form})