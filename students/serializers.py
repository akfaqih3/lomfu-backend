from rest_framework import serializers
from courses.models import(
        Course,
        Module,
)

class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ['id','title','description','order','photo']

class CourseJoinSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    owner = serializers.CharField(source='owner.name')
    subject = serializers.CharField(source='subject.title')
    class Meta:
        model = Course
        fields = ['id','title','subject','owner','overview','photo','total_students','total_modules','created','modules']