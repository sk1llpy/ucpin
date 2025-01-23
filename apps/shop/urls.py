from django.urls import path
from . import views

urlpatterns = [
    path('admin/shop/redeemcode/add/many/', views.CreateRedeemCodeView.as_view(), name="create_redeemcode"),
    path('admin/shop/redeemcode/redirect/', views.RedirectView.as_view(), name="redirect"),
]