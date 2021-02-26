from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()

class FormularioRegistroUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'rut', 'first_name', 'apellido_paterno', 
                'apellido_materno', 'resumen', 'telefono', 'sexo', 
                'estado_civil', 'direccion_calle', 'direccion_numero', 'comuna', 'asamblea')