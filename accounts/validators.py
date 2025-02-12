from rest_framework import serializers
from .models import User

class PasswordValidator:
    def __init__(self, min_length=8, max_length=64,upper=False,lower=True,number=True,special=False):
        self.min_length = min_length
        self.max_length = max_length
        self.upper = upper
        self.lower = lower
        self.number = number
        self.special = special
        
    def validate(self, password):
        if len(password) < self.min_length:
            raise serializers.ValidationError({"detail":f"Password must be at least {self.min_length} characters long"})
        if len(password) > self.max_length:
            raise serializers.ValidationError({"detail":f"Password must be at most {self.max_length} characters long"})
        if self.upper:
            if not any(char.isupper() for char in password):
                raise serializers.ValidationError({"detail":"Password must contain at least one uppercase letter"})
        if self.lower:
            if not any(char.islower() for char in password):
                raise serializers.ValidationError({"detail":"Password must contain at least one lowercase letter"})
        if self.number:
            if not any(char.isdigit() for char in password):
                raise serializers.ValidationError({"detail":"Password must contain at least one number"})
        if self.special:
            if not any(char in "!@#$%^&*()-_+=[]{}|\\:;\"'<>,.?/~`" for char in password):
                raise serializers.ValidationError({"detail":"Password must contain at least one special character"})
        
        return password
    
    def __call__(self, password):
        return self.validate(password)
    

class EmailValidator:
    
    def validate(self, email):
        if not email:
            raise serializers.ValidationError({"detail":"The given email must be set"})
        if User.objects.filter(email=email).first():
            raise serializers.ValidationError({"detail":"Email already exists"})

        return email
    
    def __call__(self, email):
        
        return self.validate(email)
    

class PhoneValidator:

    def __init__(self,length=9,allowed_prefixes=['70','71','73','77','78']):
        self.length = length
        self.allowed_prefixes = allowed_prefixes
        
    def validate(self, phone):
        if len(phone) != self.length:
            raise serializers.ValidationError({"detail":f"Phone number must be {self.length} characters long"})
        if not phone.isdigit():
            raise serializers.ValidationError({"detail":"Phone number must be a number"})
        if not any(phone.startswith(prefix) for prefix in self.allowed_prefixes):
            raise serializers.ValidationError({"detail":"Phone number invalid"})
        if User.objects.filter(phone=phone).first():
            raise serializers.ValidationError({"detail":"Phone already exists"})
        
        return phone
    
    def __call__(self, phone):
        
        return self.validate(phone)