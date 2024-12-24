from rest_framework import serializers
from .models import User,UserRole
from .validators import(
    PasswordValidator,
    EmailValidator,
    PhoneValidator
)

class UserOutputSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(source='profile.photo')
    bio = serializers.CharField(max_length=255,source='profile.bio')
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'role','photo', 'bio']

class UserInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=9, required=False)
    role = serializers.ChoiceField(choices=UserRole.choices)
    password = serializers.CharField(
        max_length=100,
        style={'input_type':'password'},
        validators=[PasswordValidator(min_length=8, max_length=64,upper=False,lower=True,number=True,special=False)]
        )
    confirm_password = serializers.CharField(max_length=100,style={'input_type':'password'})

        
    def validate(self, data):
        EmailValidator().validate(data['email'])

        if 'phone' in data:
            PhoneValidator().validate(data['phone'])
        else:
            if data['role'] == UserRole.TEACHER:
                raise serializers.ValidationError('Teachers must have a phone number')

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        
        return data
    

class OTPSendSerializer(serializers.Serializer):
    email = serializers.EmailField()

    
class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class UserUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=9, required=False)
    role = serializers.ChoiceField(choices=UserRole.choices, required=False)
    photo = serializers.ImageField(required=False)
    bio = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        
        if 'phone' in data:
            PhoneValidator().validate(data['phone'])
        else:
            if data['role'] == UserRole.TEACHER:
                raise serializers.ValidationError('Teachers must have a phone number')
                
        return data
    


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100,style={'input_type':'password'},validators=[PasswordValidator()])
    new_password = serializers.CharField(max_length=100,style={'input_type':'password'},validators=[PasswordValidator()])
    confirm_password = serializers.CharField(max_length=100,style={'input_type':'password'},validators=[PasswordValidator()])

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data