from django.shortcuts import render
from django.views import View
from django.http import HttpRequest

# Create your views here.
class PageNotFoundView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        return render(request, '404.html', status=404)