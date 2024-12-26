from django.urls import path, include
from .views import (
    CourseCreateAPI,
    CourseListAPI,
    CourseDetailAPI,
    CourseUpdateAPI,    
    CourseDeleteAPI,
)

urlpatterns = [
    path('courses/', CourseListAPI.as_view()),
    path('courses/create/', CourseCreateAPI.as_view()),
    path('courses/<int:pk>/', CourseDetailAPI.as_view()),
    path('courses/<int:pk>/update/', CourseUpdateAPI.as_view()),
    path('courses/<int:pk>/delete/', CourseDeleteAPI.as_view()),
   
]