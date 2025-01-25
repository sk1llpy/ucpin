from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse

from . import models


# Create your views here.
class RedirectView(View):
    def get(self, request: HttpRequest):
        if request.user:
            if request.user.is_superuser:
                return render(request, 'redirect.html')
            else:
                return HttpResponse("<h1>404 | Page not found<h1>")
        else:
            return HttpResponse("<h1>404 | Page not found<h1>")


class CreateRedeemCodeView(View):
    def get(self, request: HttpRequest):
        if request.user:
            if request.user.is_superuser:
                packages = models.UCPackage.objects.all()

                return render(request, 'redeem_code.html', context={"packages": packages})
            else:
                return HttpResponse("<h1>404 | Page not found<h1>")
        else:
            return HttpResponse("<h1>404 | Page not found<h1>")
    
    def post(self, request: HttpRequest):
        codes: str = request.POST.get('code')
        package: int = request.POST.get('package')

        codes = codes.split()
        error = False

        for code in codes:
            try:
                package_obj = models.UCPackage.objects.get(pk=package)
                obj = models.RedeemCode.objects.create(
                    code=code,
                    package=package_obj,
                    is_used=False,
                )
                obj.save()
            except:
                error = True
                break
        
        if error:
            packages = models.UCPackage.objects.all()
            return render(request, 'redeem_code.html', context={"packages": packages, "error": "Redeem-code allaqachon mavjud!"})
        else:
            return redirect('redirect')