from rest_framework import serializers
from .models import User,Profile,UserRole
import re


class ProfileOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo', 'bio']

class UserOutputSerializer(serializers.ModelSerializer):
    profile = ProfileOutputSerializer()
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'role', 'profile']

class UserInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=9, required=False)
    role = serializers.ChoiceField(choices=UserRole.choices)
    password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

    def validate_name(self, name):
        if len(name) < 3:
            raise serializers.ValidationError('Name must be at least 3 characters long')
        
        return name
    
    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError('The given email must be set')
        if User.objects.filter(email=email).first():
            raise serializers.ValidationError('Email already exists')

        return email
        
    def validate_phone(self, phone):
        if len(phone) != 9:
            raise serializers.ValidationError('Phone number must be 9 characters long')
        if not re.search(r'^7[01387]', phone):
            raise serializers.ValidationError('Phone number invalid')
        if User.objects.filter(phone=phone).first():
            raise serializers.ValidationError('Phone already exists')
        
        return phone
    
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', password):        
            raise serializers.ValidationError('Password must contain at least one number')
        
        return password
        
    def validate(self, data):
        data['name'] = self.validate_name(data['name'])
        data['email'] = self.validate_email(data['email'])

        if 'phone' in data:
            data['phone'] = self.validate_phone(data['phone'])
        else:
            if data['role'] == UserRole.TEACHER:
                raise serializers.ValidationError('Teachers must have a phone number')

        data['password'] = self.validate_password(data['password'])
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        
        return data
    


class UserUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=9, required=False)
    role = serializers.ChoiceField(choices=UserRole.choices, required=False)
    photo = serializers.ImageField(required=False)
    bio = serializers.CharField(max_length=255, required=False)





class OTPSendSerializer(serializers.Serializer):
    email = serializers.EmailField()

    
class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)