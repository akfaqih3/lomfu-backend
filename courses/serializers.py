from rest_framework import serializers

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

        

class CourseInputSerializer(serializers.Serializer):
    subject = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Subject.objects.all(),
        required=True
    )
    title = serializers.CharField(max_length=200)
    overview = serializers.CharField(max_length=255)
    photo = serializers.ImageField(required=False)


class CourseOutputSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.title')
    class Meta:
        model = Course
        fields = ['title', 'slug', 'subject', 'overview', 'photo','created']