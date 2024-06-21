from django.core.handlers import wsgi
import json
class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request (e.g., log IP address)
        client_ip = RequestLoggerMiddleware.get_client_ip(request)
        print(f"\tRequest from IP: {client_ip}")
        response = self.get_response(request)

        return response
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

