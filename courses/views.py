from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from .models import (
    Subject,
  
)
from .serializers import (
    SubjectsOutputSerializer,
    SubjectCoursesOutputSerializer,
)

class SubjectViewSet(viewsets.ViewSet):
    
    queryset = Subject.objects.all()
    serializer_class = SubjectsOutputSerializer
    retrieve_serializer_class = SubjectCoursesOutputSerializer

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request,slug):
        subject = self.queryset.get(slug=slug)
        queryset = subject.courses.all()
        serializer =self.retrieve_serializer_class(queryset, many=True)

        return Response(
            {
                'subject': subject.title,
                'courses': serializer.data
            }
        )