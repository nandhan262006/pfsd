from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('services.urls')),
    path('', include('accounts.urls')),
    path('', include('reviews.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site header
admin.site.site_header = "ProConnect Administration"
admin.site.site_title = "ProConnect Admin"
admin.site.index_title = "Welcome to ProConnect Admin Panel"
