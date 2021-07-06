from django.urls import path
from .views import googleSocialAuth

urlpatterns = [
    path('google/',googleSocialAuth)
]
