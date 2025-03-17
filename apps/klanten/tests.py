# Tests voor klanten
# voorbeeld: apps/klanten/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Klant

class KlantTests(TestCase):
    def test_klant_aanmaken(self):
        response = self.client.post(reverse('klanten:create'), {
            'naam': 'Test Klant',
            'adres': 'Straat 123',
            'woonplaats': 'Plaats',
            # voeg hier meer velden toe...
        })
        self.assertEqual(response.status_code, 302)  # redirect verwacht
        self.assertTrue(Klant.objects.filter(naam='Test Klant').exists())
