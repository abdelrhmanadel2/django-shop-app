from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            # idinfo=id_token.verify_oauth2_token(auth_token)
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if idinfo['iss'] in ['https://accounts.google.com',]:
                return idinfo
            

               # Or, if multiple clients access the backend server:
    # idinfo = id_token.verify_oauth2_token(token, requests.Request())
    # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
    #     raise ValueError('Could not verify audience.')

    # If auth request is from a G Suite domain:
    # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
    #     raise ValueError('Wrong hosted domain.')

    # ID token is valid. Get the user's Google Account ID from the decoded token.

        except:
            return "The token is either invalid or has expired"
