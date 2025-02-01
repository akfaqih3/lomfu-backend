from django.conf import settings
import requests
from rest_framework import serializers


class GoogleOAuth2:
    def __init__(self,code):
        self.code = code
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.access_token_url = 'https://accounts.google.com/o/oauth2/token'
        self.user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'

    def get_access_token(self):
        try:
            data = {
                'code': self.code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.redirect_uri,
                'grant_type': 'authorization_code'
            }
            response = requests.post(self.access_token_url, data=data)
            return response.json()
        except Exception as e:
            raise serializers.ValidationError({"detail":e})
    
    def get_user_info(self):
        try:
            access_token = self.get_access_token()
            data = {
                'access_token': access_token['access_token']
            }
            response = requests.get(self.user_info_url, params=data)
            return response.json()
        except Exception as e:
            raise serializers.ValidationError({"detail":e})

    def get_user(self):
        return self.get_user_info()