from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "PSU Complaints Administration"
admin.site.site_title = "PSU Admin Portal"
admin.site.index_title = "Welcome to PSU Complaints Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('complaints.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
