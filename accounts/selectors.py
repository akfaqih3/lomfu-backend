from rest_framework import permissions
from .models import User, Profile
from rest_framework import serializers

def user_by_id(id):
    try:
        user = User.objects.get(id=id)
    except:
        raise serializers.ValidationError("Not Found.")
    
    return user
