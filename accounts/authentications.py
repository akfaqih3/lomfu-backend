from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from .utils import LimitLoginAttempt
from .services import send_otp
from rest_framework.exceptions import (
    NotAuthenticated
)

User = get_user_model()

loginAttempt = LimitLoginAttempt()

class CustomAuthentication(BaseBackend):
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        
        if not email:
            email = kwargs.get('username').strip()

        try:
            user = User.objects.get(
                Q(email=email) | Q(phone=email)  
            )
        except User.DoesNotExist:
            return None

        
        loginAttempt(user.email)
        
        if user.check_password(password):
            if not user.is_active and user.last_login is None:
                send_otp(user.email)
                raise NotAuthenticated({"detail":"Account is not verified."})
            loginAttempt.clear()
            return user
        loginAttempt.attempt()

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
