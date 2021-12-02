from django.urls import path, include

from .views import UserAPIView

urlpatterns = [
    path('user/', UserAPIView.as_view())
]