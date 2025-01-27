from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),  # Assuming your API routes are here
    path('', RedirectView.as_view(url='api/login/')),  # Redirect root to login
    path('accounts/', include('allauth.urls')),  # Include allauth URLs
]