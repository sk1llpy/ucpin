from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.shop.urls')),

    # Admin-panel
    path('admin/', admin.site.urls),
]
