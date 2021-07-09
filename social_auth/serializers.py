from social_auth import facebook
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from . import google, facebook
from .register import *

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != '1022319866638-hht9tl3dkrl0j1ikcmvckld15nql89kg.apps.googleusercontent.com':
        # os.environ.get('GOOGLE_CLIENT_ID'):

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
    
        email = user_data['email']
        first_name=user_data['given_name']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name, first_name=first_name)


class FacebookSerializer(serializers.Serializer):
    auth_token=serializers.CharField()
    
    def validate_auth_token(self, auth_token):
        print(auth_token)
        user_data=facebook.Facebook.validate(auth_token)
       
        user_id = user_data['id']
        email=user_data['email']
        first_name=user_data['name']
        name=user_data['name']
        provider='facebook'
        return register_social_user(

        provider=provider, user_id=user_id, email=email, name=name, first_name=first_name)

    