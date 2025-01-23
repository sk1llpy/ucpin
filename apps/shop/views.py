from django.shortcuts import render, redirect
from django.views import View

from . import models


# Create your views here.
class RedirectView(View):
    def get(self, request):
        return render(request, 'redirect.html')


class CreateRedeemCodeView(View):
    def get(self, request):
        packages = models.UCPackage.objects.all()

        return render(request, 'redeem_code.html', context={"packages": packages})
    
    def post(self, request):
        codes: str = request.POST.get('code')
        package: int = request.POST.get('package')

        codes = codes.split()

        for code in codes:
            package_obj = models.UCPackage.objects.get(pk=package)
            obj = models.RedeemCode.objects.create(
                code=code,
                package=package_obj,
                is_used=False,
            )
            obj.save()
        
        return redirect('redirect')