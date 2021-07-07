from account.serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.serializers import Serializer
from account.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name, first_name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password='ddd')
            serializer=UserSerializer(registered_user,  many=False)
            return {
                'user': serializer.data,
                'Token':str(AccessToken.for_user(registered_user))

                }

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + str(filtered_user_by_email[0].auth_provider))

    else:
        user = {
            'username': generate_username(name), 'email': email,'first_name':first_name,
            'password': 'ddd'}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        # new_user = authenticate(
        #     email=email, password=os.environ.get('SOCIAL_SECRET'))
        return {
            'user':UserSerializer(user,many=False).data,
            'Token':str(AccessToken.for_user(user))
            }