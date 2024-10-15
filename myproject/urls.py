from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Route for the Django admin panel
    path('', include('myapp.urls')),  # Include the URLs from the 'myapp' app
]
