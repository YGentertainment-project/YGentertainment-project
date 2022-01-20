from django.test import TestCase
from django.test import Client


# Create your tests here.
class ArtistTest(TestCase):
    def setUP(self):
        client = Client()
        return client

    def test_get_artist_view(self):
        response = self.client.get("api/artist/")
        self.assertEqual(response.status, 200)
