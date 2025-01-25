from django.urls import path
from . import views

urlpatterns = [
    path('shop/redeemcode/add/many/', views.CreateRedeemCodeView.as_view(), name="create_redeemcode"),
]