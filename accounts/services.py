from .models import User, Profile


def user_create(name, email, role, password, phone=None):
    
    user = User.objects.create_user(email, password)
    user.name = name
    if phone is not None:
        user.phone = phone
    user.role = role
    user.save()
    profile_create(user, None, None)
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