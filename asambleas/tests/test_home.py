from django.test import TestCase
from django.urls import reverse

class PrincipalTest(TestCase):
    def test_principal_view(self):
        response = self.client.get(reverse('asambleas:principal'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")