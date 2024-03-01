from django.test import TestCase
from django.urls import reverse
from .models import ShortUrlModel
from .views import generate_short_code


class ShortUrlModelTestCase(TestCase):
    def test_short_code_generation(self):
        # Test if the short code is generated correctly
        original_url = "http://example.com"
        short_code = generate_short_code(original_url)
        self.assertEqual(len(short_code), 12)

    def test_shorten_url_view(self):
        # Test the shorten URL view
        response = self.client.post("/shorten/", {"original_url": "http://example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("short_code", response.data)

    def test_redirect_to_url_view(self):
        # Test the redirect to URL view
        short_url = ShortUrlModel.objects.create(
            original_url="http://example.com", short_code="test123456"
        )
        response = self.client.get(
            reverse("redirect_url", kwargs={"short_code": "test123456"})
        )
        self.assertEqual(response.status_code, 302)
