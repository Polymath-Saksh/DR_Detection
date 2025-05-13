from django.urls import path

from . import views  # Import views from the current app

urlpatterns = [
    # Example URL patterns
    path('', views.detector, name='detector'),  # Detection2 view
]