from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AnonymousUserTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_anonymous_user_can_access_public_page(self):
        # Test that an anonymous user can access the public page
        response = self.client.get(reverse('asambleas:principal'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_anonymous_user_cannot_access_secret_page(self):
        # Test that an anonymous user is redirected to the login page for the secret page
        response = self.client.get(reverse('asambleas:ver_secciones_individuales_de_asamblea'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/ver_secciones_individuales_de_asamblea')
