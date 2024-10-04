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
import time


class StatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        response["X-Page-Generation-Duration-ms"] = int(duration * 1000)
        print('Hi')
        return response