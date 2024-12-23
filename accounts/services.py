from .models import User, Profile
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from .utils import OTP_manager
from rest_framework import serializers

def user_create(name, email, role, password, phone=None):
    
    user = User.objects.create_user(email, password)
    user.name = name
    if phone is not None:
        user.phone = phone
    user.role = role
    user.save()
    profile_create(user, None, None)
    send_otp(user.email)
    return user


def user_update(user, name, email, role, phone=None,photo=None,bio=None):
    user.name = name
    user.email = email
    user.role = role
    if phone is not None:
        user.phone = phone
    user.save()
    profile_update(user, photo, bio)
    return user


def user_delete(user):
    if profile_delete(user):
        user.delete()
        return True
    return False



def profile_create(user, photo, bio):
    profile = Profile.objects.create(user=user)
    profile.photo = photo
    profile.bio = bio
    profile.save()    
    return profile

def profile_update(user, photo, bio):
    profile = Profile.objects.get(user=user)
    profile.photo = photo
    profile.bio = bio
    profile.save()    
    return profile

def profile_delete(user):
    profile = Profile.objects.get(user=user)
    profile.delete()
    return True




def send_otp(email: str):
    otp = OTP_manager()
    user = get_object_or_404(User, email=email)
    if user.is_active:
        raise serializers.ValidationError("has already been verified.")
    otp_code = otp.generate_otp(email)
    send_mail(
        subject='OTP for Yemen Eroud',
        message=f'Your OTP is {otp_code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    return otp_code

def verify_otp(email: str, otp: str):
    user = get_object_or_404(User, email=email)
    otp_manager = OTP_manager()
    if otp_manager.verify_otp( user.email, otp):
        user.is_active= True
        user.save()
        return user
    raise serializers.ValidationError("Invalid OTP.")