from django.db import models
import base64
import random
import string

def generate_short_code(original_url):
    """
    Generates a unique short code for a URL using base64 encoding.

    Combines a shortened base64-encoded version of the original URL and a
    random suffix to improve uniqueness and maintain readability.

    Args:
        original_url: The original URL to shorten.

    Returns:
        A unique short code string.
    """

    while True:
        short_url =base64.urlsafe_b64encode(original_url.encode('utf-8')).decode('utf-8')[:6]
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        short_code = f"{short_url}{random_suffix}"

        if not ShortUrlModel.objects.filter(short_code=short_code).exists():
            return short_code

class ShortUrlModel(models.Model):
    original_url = models.URLField(max_length=2000, unique=True)
    short_code = models.CharField(max_length=12, unique=True, default=generate_short_code)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_url} -> {self.short_code}"
