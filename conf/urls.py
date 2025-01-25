from django.contrib import admin
from django.urls import path, include
from apps.general.views import PageNotFoundView

urlpatterns = [
    path('', include('apps.shop.urls')),

    # Admin-panel
    path('', admin.site.urls),
]

handler404 = PageNotFoundView.as_view()
