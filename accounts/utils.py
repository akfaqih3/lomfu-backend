import pyotp
from django.core.cache import cache
from rest_framework import serializers

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