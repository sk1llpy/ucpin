from django.urls import path
from . import views

urlpatterns = [
    path('redeemcode/add/many/', views.CreateRedeemCodeView.as_view(), name="create_redeemcode"),
]