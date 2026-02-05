from django.urls import path
from .views import HoneypotAPIView

urlpatterns = [
    path('honeypot', HoneypotAPIView.as_view(), name='honeypot'),
]
