from inspect import getcomments
from .views import *
from account.views import *
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('products/', getProducts, name="products"),
    path('user/profile/', getUserProfile, name="user_profile"),
    path('register/', register, name='register'),
    path('users/', getUser, name='users'),
    path('login/', login, name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email', verifyEmail, name='verify-email'),
    path('makefavorite/', addFavorite,name='makefavorite'),
    path('category/',categoryView, name='categoryView' ),
    # path('<str:category_name>',categoryProducts )
    path('comments/<int:id>',productComments, name='comments'),
    path('like/',likeComment,name='like'),
    path('dislike/',dislikedComment,name='like')

]
