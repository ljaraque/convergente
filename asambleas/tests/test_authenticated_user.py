from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from gestion.models import Rol, Asamblea
from .utilities import BaseDataTestCase

User = get_user_model()


class AuthenticatedUserTest(BaseDataTestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="Neo1",
            first_name="Neo1",
            apellido_paterno="NeoAp",
            apellido_materno="NeoAp",
            resumen="Soy Neo",
            telefono="+56000000000",
            sexo=User.FEMENINO,
            estado_civil=User.SOLTERO,
            direccion_calle="Calle",
            direccion_numero="000",
            es_representante=True,
            comuna=Asamblea.objects.all()[0].comuna,
            asamblea=Asamblea.objects.all()[0],
            password="1234", 
            rol=Rol.objects.get(nombre="Representante")
        )
        self.client.login(username="Neo1", password="1234")

    def test_authenticated_user_can_access_public_page(self):
        # Test that an authenticated user can access the public page
        response = self.client.get(reverse('asambleas:principal'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logout")

    def test_authenticated_user_can_access_secret_page(self):
        # Test that an authenticated user can access the secret page
        response = self.client.get(
            reverse('asambleas:ver_secciones_individuales_de_asamblea')
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logout")



