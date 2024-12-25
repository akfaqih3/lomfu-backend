from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CourseInputSerializer,
    CourseOutputSerializer,
)
from .permissions import (
    IsTeacher,
    IsOwner,
)
from .services import (
    course_create,
    course_update,
    course_delete,
)
from .selectors import (
    course_list,
    course_detail,
)

class CourseCreateAPI(APIView):
    permission_classes = [
        IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = CourseInputSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            course = course_create(
                owner=request.user,
                subject=serializer.data['subject'],
                title=serializer.data['title'],
                overview=serializer.data['overview'],
                photo=serializer.data['photo'] | None
            )
            serializer = self.serializer_class(course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseListAPI(APIView):
    permission_classes = [
        IsAuthenticated,
        IsTeacher,
    ]
    serializer_class = CourseOutputSerializer

    def get_queryset(self):
        return course_list(owner=self.request.user)

    def get(self, request):
        courses = self.get_queryset()
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CourseDetailAPI(APIView):
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]
    serializer_class = CourseOutputSerializer

    def get_object(self, slug):
        coures = course_detail(slug=slug)
        self.check_object_permissions(self.request, coures)
        return coures

    def get(self, request, slug):
        course = self.get_object(slug)
        serializer = self.serializer_class(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CourseUpdateAPI(APIView):
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]
    serializer_class = CourseInputSerializer
    
    def put(self, request, slug):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            course = course_update(
                slug=slug,
                subject=serializer.data['subject'],
                title=serializer.data['title'],
                overview=serializer.data['overview'],
                photo=serializer.data['photo'] | None
            )
            serializer = self.serializer_class(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDeleteAPI(APIView):
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]

    def get_object(self, slug):
        course = course_detail(slug=slug)
        self.check_object_permissions(self.request, course)
        return course
    
    def delete(self, request, slug):
        course_delete(self.get_object(slug))
        return Response(status=status.HTTP_204_NO_CONTENT)