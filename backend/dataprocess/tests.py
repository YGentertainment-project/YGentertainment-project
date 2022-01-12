from django.http import response
from django.test import TestCase
from django.test import Client
from .models import *


# Create your tests here.
class ArtistTest(TestCase):
    def setUP(self):
        client = Client()
    

    def test_get_artist_view(self):
        response = self.client.get('api/artist/')
        self.assertEqual(response.status,200)
    