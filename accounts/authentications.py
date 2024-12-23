from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from .utils import LimitLoginAttempt


User = get_user_model()

login = LimitLoginAttempt()

class CustomAuthentication(BaseBackend):
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        email = email.strip()

        try:
            user = User.objects.get(
                Q(email=email) | Q(phone=email)  
            )
        except User.DoesNotExist:
            return None

        
        login(user.email)
        
        if user.check_password(password):
            login.clear()
            return user
        login.attempt()
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
