import re
from itertools import cycle

from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError # para validadores
from django.contrib.auth.forms import AuthenticationForm, UsernameField

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='RUT',
        widget=forms.TextInput(attrs={'autofocus': True})
    )



class FormularioRegistroUser(UserCreationForm):
    error_messages = {
        'duplicate_username': 'El identificador de usuario ingresado ya existe, inténte nuevamente'
    }

    username = forms.CharField(max_length=50, help_text="Su Usuario debe ser su rut completo (Con digito verificador)", label = "RUT")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'apellido_paterno', 
                'apellido_materno', 'telefono', 'sexo', 
                'estado_civil', 'direccion_calle', 'direccion_numero', 'asamblea')
        labels = {'email': 'Email'}

    # Validador rut
    def valida_username(self, username):
        username_clean = (re.sub("[^0-9kK]", "", str(username))).lower()
        if username_clean.count("k")>0:
            if username_clean.count("k")>1 or username_clean[-1]!="k":
                raise ValidationError("formato de RUT incorrecto")
        print("username_clean", username_clean)
        if len(username_clean)<8 or len(username_clean)>9:
            raise ValidationError("El número de digitos ingresados no es correcto!") 
        username_clean_no_digit = int(username_clean[:-1])
        reversed_digits = map(int, reversed(str(username_clean_no_digit)))
        factors = cycle(range(2, 8))
        s = sum(d * f for d, f in zip(reversed_digits, factors))
        digit = (-s) % 11
        print(digit)
        if digit == 10:
            digit="k"
        if str(digit)==username_clean[-1]:
            return username_clean
        else: 
            raise ValidationError("El Digito Verificador no corresponde!") 


    def clean_username(self):
        username = self.cleaned_data["username"]
       
        try:
            username = self.valida_username(username)
            User._default_manager.get(username=username)
            #if the user exists, then let's raise an error message

            raise forms.ValidationError( 
              self.error_messages['duplicate_username'],  #user my customized error message

              code='duplicate_username',   #set the error message key

                )
        except User.DoesNotExist:
            return username # great, this user does not exist so we can continue the registration process


