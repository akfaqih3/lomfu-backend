from rest_framework import serializers
from .models import (
    Subject,
    Course,
    Module,
    Content,
    ItemBase,
    Text,
    File,
    Image,
    Video,
)
class SubjectsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Subject
            fields = ['title', 'slug','photo', 'total_courses']

class SubjectCoursesOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title',  'overview', 'photo','created']