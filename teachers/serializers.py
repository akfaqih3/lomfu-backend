from rest_framework import serializers

from courses.models import (
    Subject,
    Course,
)

        

class CourseInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
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
        fields = ['id','title', 'subject', 'overview', 'photo','created']