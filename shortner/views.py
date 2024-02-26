from .models import ShortUrlModel,generate_short_code
from rest_framework.views import APIView
from rest_framework.response import Response

class ShortenUrl(APIView):
    def post(self, request):
        original_url = request.data.get('original_url')
        if not original_url:
            return Response({'error': 'Missing original URL'}, status=400)
        try:
            short_url = ShortUrlModel.objects.get(original_url=original_url)
            short_code = short_url.short_code
            return Response({'short_code': short_code})
        except ShortUrlModel.DoesNotExist:
            short_code = generate_short_code(original_url)
            short_url = ShortUrlModel.objects.create(original_url=original_url,short_code=short_code)
            return Response({'short_code': short_code})
        
class RedirectToUrl(APIView):
    def get(self, request, short_code):
        try:
            short_url = ShortUrlModel.objects.get(short_code=short_code)
            return Response({'original_url': short_url.original_url}, status=302) #302 will redirect to original url
        except ShortUrlModel.DoesNotExist:
            return Response({'error': 'Invalid short code'}, status=404)


