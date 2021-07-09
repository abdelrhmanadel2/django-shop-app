from django.urls import path
from .views import facebookSocialAuth, googleSocialAuth

urlpatterns = [
    path('google/',googleSocialAuth),
    path('facebook/',facebookSocialAuth),
]
