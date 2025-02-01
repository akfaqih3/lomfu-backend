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



class CourseSerializer(serializers.ModelSerializer):
        subject = serializers.CharField(source='subject.title')
        owner = serializers.CharField(source='owner.name')
        class Meta:
            model = Course
            fields = ['id','owner','title','subject', 'overview', 'photo','total_students','total_modules','created']