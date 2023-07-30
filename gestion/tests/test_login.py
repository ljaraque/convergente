from django.urls import reverse
from django.contrib.auth import get_user_model
from gestion.models import Rol
from .utilities import BaseDataTestCase

User = get_user_model()


class LoginTests(BaseDataTestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'

        self.user = User.objects.create_user(
            username=self.username ,
            first_name="admin",
            apellido_paterno="admin",
            apellido_materno="admin",
            resumen="Soy el administrador",
            telefono="+56000000000",
            sexo=User.FEMENINO,
            estado_civil=User.SOLTERO,
            direccion_calle="Calle",
            direccion_numero="000",
            es_representante=False,
            comuna=None,
            asamblea=None,
            password='testpass', 
            rol=Rol.objects.get(nombre="Administrador")
        )

    def test_login_successful(self):
        response = self.client.post(
            reverse('login'), 
            {'username': self.username, 
             'password': self.password}
        )
        # check redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('asambleas:principal'))

    def test_login_failed(self):
        response = self.client.post(
            reverse('login'), 
            {'username': self.username, 'password': 'wrongpassword'}
        )
        self.assertEqual(response.status_code, 200)  # Expect the same login page to be re-rendered
        #self.assertContains(response, 'Invalid credentials.')  # Replace with your error message for login failure

