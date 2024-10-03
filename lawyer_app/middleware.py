from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response