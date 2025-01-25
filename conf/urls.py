from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.general.views import PageNotFoundView

urlpatterns = [
    path('shop/', include('apps.shop.urls')),
    
    # Admin-panel
    path('', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = PageNotFoundView.as_view()

