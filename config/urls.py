from django.contrib import admin
from django.urls import path, include

domain_url = "api/v1"

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f"{domain_url}/", include('core.urls')),
    path(f"{domain_url}/auth/", include('accounts.urls')),
]
