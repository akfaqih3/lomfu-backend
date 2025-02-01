from rest_framework.exceptions import ValidationError
from courses.models import (
    Subject,
    Course,
)


def course_list(owner):
    try:
        courses = Course.objects.filter(owner=owner)
    except Exception as e:
        raise ValidationError({"detail":e})
    
    return courses
    
def course_detail(pk):
    try:
        course = Course.objects.get(pk=pk)
    except Exception as e:
        raise ValidationError({"detail":e})
    
    return course