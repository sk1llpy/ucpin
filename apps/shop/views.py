from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest

from . import models


# Create your views here.
class CreateRedeemCodeView(View):
    def get(self, request: HttpRequest):
        if request.user:
            if request.user.is_superuser:
                packages = models.UCPackage.objects.all()

                return render(request, 'redeem_code.html', context={"packages": packages})
            else:
                return redirect('admin:login')
        else:
            return redirect('admin:login')
    
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
            return render(request, 'redeem_code.html', context={"success": True})