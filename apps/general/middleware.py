from django.http import HttpResponseNotFound
from django.shortcuts import render

class PageNotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if it's a 404 response and handle it with a custom 404 page
        if response.status_code == 404:
            return render(request, '404.html', status=404)
        
        return response
