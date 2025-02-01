from rest_framework.exceptions import ValidationError
from courses.models import (
    Subject,
    Course,
)



def course_create(owner,subject, title, overview, photo=None):
    try:
        subject = Subject.objects.get(slug=subject)
        course = Course.objects.create(
            owner=owner,
            subject=subject,
            title=title,
            overview=overview,
            photo=photo
            )
    except Exception as e:
        raise ValidationError({"detail":e})
    
    return course

def course_update(pk,subject=None, title=None, overview=None, photo=None):
    
    try:
        course = Course.objects.get(pk=pk)
        if subject is not None and subject != course.subject.slug:
            course.subject = Subject.objects.get(slug=subject)
        if title is not None:
            course.title = title
        if overview is not None:
            course.overview = overview
        if photo is not None:
            course.photo = photo
        course.save()
    except Exception as e:
        raise ValidationError({"detail":e})
    
    return course

def course_delete(course):
    try:
        course.delete()
    except Exception as e:
        raise ValidationError({"detail":e})