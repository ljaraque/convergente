from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Rol, Comuna
import re 

User = get_user_model()


# Create your views here.


from django.contrib.auth.views import LoginView

from .forms import CustomAuthenticationForm


###############################################################################
# Login Usuario
###############################################################################

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm



###############################################################################
# Registro de Usuario
###############################################################################

from .forms import FormularioRegistroUser
def registro(request):
    if request.method == 'POST':
        form = FormularioRegistroUser(request.POST)
        if form.is_valid():
            rol = Rol.objects.get(nombre="Miembro")
            asamblea = form.cleaned_data.get('asamblea')
            username = form.cleaned_data.get('username')
            username_clean = re.sub("[^0-9]", "", str(username))
            User.objects.create_user(username=username,
                                    first_name=form.cleaned_data.get('first_name'),
                                    apellido_paterno=form.cleaned_data.get('apellido_paterno'),
                                    apellido_materno=form.cleaned_data.get('apellido_materno'),
                                    resumen=form.cleaned_data.get('resumen'),
                                    telefono=form.cleaned_data.get('telefono'),
                                    sexo=form.cleaned_data.get('sexo'),
                                    estado_civil=form.cleaned_data.get('estado_civil'),
                                    direccion_calle=form.cleaned_data.get('direccion_calle'),
                                    direccion_numero=form.cleaned_data.get('direccion_numero'),
                                    comuna=asamblea.comuna, #form.cleaned_data.get('comuna'),
                                    asamblea=asamblea, #form.cleaned_data.get('asamblea'),
                                    password=form.cleaned_data.get('password1'), 
                                    rol=rol)
            #user = authenticate(username=username, password=raw_password, rol="subcliente")
            #login(request, user)
            #list(messages.get_messages(request))
            #messages.success(request, "El usuario fué creado exitósamente!")
            return redirect('asambleas:principal')
    else:
        form = FormularioRegistroUser()
    return render(request, 'gestion/usuario_registro.html', {'form': form})

###############################################################################
# Gestion Representante -- Miembro
###############################################################################

