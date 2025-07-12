from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

import products
from products import views
from shop_app import settings

urlpatterns = [
    path("", include("products.urls")),
    path("cart/", include("cart.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
