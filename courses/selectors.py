from rest_framework.exceptions import ValidationError
from .models import (
    Subject,
    Course,
    Module,
    Content,
    Text,
    File,
    Image,
    Video
)


def course_list(owner):
    try:
        courses = Course.objects.filter(owner=owner)
    except Exception as e:
        raise ValidationError(e)
    
    return courses
    
def course_detail(slug):
    try:
        course = Course.objects.get(slug=slug)
    except Exception as e:
        raise ValidationError(e)
    
    return course