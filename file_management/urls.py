from django.contrib import admin
from django.urls import path, include
from file_management_app import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('file_management/', include(urls)),
]