from .models import User, Profile
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from .utils import OTP_manager
from rest_framework import serializers
from django.contrib.auth.models import Group

def user_create(name, email, role, password, phone=None):
    
    try:
        user = User.objects.create_user(email, password)
        user.name = name if name else None
        if phone is not None:
            user.phone = phone
        user.role = role
        user.groups.clear()
        user.groups.add(Group.objects.get(name=role))
        user.save()
    except Exception as e:
        raise serializers.ValidationError(e)
    
    profile_create(user, None, None)
    send_otp(user.email)
    return user


def profile_create(user, photo, bio):
    profile = Profile.objects.create(user=user)
    profile.photo = photo
    profile.bio = bio
    profile.save()    
    return profile


def send_otp(email: str):
    otp = OTP_manager()
    user = get_object_or_404(User, email=email)
    if user.is_active:
        raise serializers.ValidationError("has already been verified.")
    otp_code = otp.generate_otp(email)
    send_mail(
        subject='OTP for lomfu',
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


def user_update(user, name=None, email=None, phone=None, role=None, photo=None, bio=None):
    if name is not None:
        user.name = name
    if email is not None:
        if User.objects.exclude(id=user.id).filter(email=email).first():
            raise serializers.ValidationError('Email already exists')
    if phone is not None:
        user.phone = phone
    if role is not None:
        user.role = role
        user.groups.clear()
        user.groups.add(Group.objects.get(name=role))

    if photo is not None:
        user.profile.photo = photo
    if bio is not None:
        user.profile.bio = bio
    user.profile.save()
    user.save()
    return user


def user_change_password(user, old_password, new_password):
    if not user.check_password(old_password):
        raise serializers.ValidationError("Invalid old password")
    user.set_password(new_password)
    user.save()
    return user