import pyotp
from django.core.cache import cache
from rest_framework import serializers
from rest_framework import status
from django.utils.timezone import now ,timedelta
from django.conf import settings

LOGIN_ATTEMPT_LIMIT = settings.LOGIN_ATTEMPT_LIMIT
LOGIN_BLOCK_TIME = settings.LOGIN_BLOCK_TIME
LOGIN_ATTEMPT_EXPIRE_TIME = settings.LOGIN_ATTEMPT_EXPIRE_TIME


class LimitLoginAttempt:
    
    def __init__(self, attempts_limit=LOGIN_ATTEMPT_LIMIT, block_time=LOGIN_BLOCK_TIME, expire_time=LOGIN_ATTEMPT_EXPIRE_TIME):
        self.attempts_limit = attempts_limit
        self.block_time =  block_time
        self.expire_time =  expire_time


    def __call__(self, identifier):
        
        self.block_key = f"block_{identifier}"
        block_data = cache.get(self.block_key)
        if block_data:
            block_end_time = block_data["end_time"]
            time_remaining = block_end_time - now()
            mins_remaining = int(time_remaining.total_seconds() / 60)
            
            raise serializers.ValidationError(
                {"message":f"Account temporarily locked. Try again after {mins_remaining} minutes."},
                status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        self.attempt_key = f"attempt_{identifier}"
        
    def clear(self):
        cache.delete(self.attempt_key)
        
    def attempt(self):
        attempts = cache.get(self.attempt_key,0)
        attempts += 1
        if attempts >= self.attempts_limit :
            block_end_time = now() + timedelta(minutes=self.block_time)
            cache.set(self.block_key,{'end_time':block_end_time},timeout=self.block_time*60)
            cache.delete(self.attempt_key)

            raise serializers.ValidationError(
                {"message":f"Too many failed login attempts. Account locked for {self.block_time} minutes."},
                status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        cache.set(self.attempt_key,attempts,timeout=self.expire_time*60)
        
        raise serializers.ValidationError(
            {"message":f"Invalid credentials. Try again. You have {self.attempts_limit - attempts} attempts remaining."},
            status.HTTP_401_UNAUTHORIZED
        )
    




class OTP_manager:
    
    def generate_otp(self,identifier):
        otp = pyotp.TOTP(pyotp.random_base32(), interval=300)
        otp_code = otp.now()
        cache.set(identifier, otp_code, 300)
        return otp_code
    
    def verify_otp(self, identifier, otp_code):
        
        if not cache.get(identifier):
            raise serializers.ValidationError(f"invalid {identifier}.")
        
        if cache.get(identifier) == otp_code:
            cache.delete(identifier)
            return True
        
        return False
    
