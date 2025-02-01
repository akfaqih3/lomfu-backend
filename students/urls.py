from django.urls import path
from .views import (
    CourseEnrollAPI,
    CoursesEnrolledAPI,
)

urlpatterns = [
    path('courses/enroll/<int:pk>/', CourseEnrollAPI.as_view()),
    path('courses/enrolled/', CoursesEnrolledAPI.as_view()),
]