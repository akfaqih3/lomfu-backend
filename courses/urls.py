from django.urls import path, include
from .views import (
    CourseCreateAPI,
    CourseListAPI,
    CourseDetailAPI,
    CourseUpdateAPI,    
    CourseDeleteAPI,
)

urlpatterns = [
    path('', CourseListAPI.as_view()),
    path('<slug>/', CourseDetailAPI.as_view()),
    path('create/', CourseCreateAPI.as_view()),
    path('<slug>/update/', CourseUpdateAPI.as_view()),
    path('<slug>/delete/', CourseDeleteAPI.as_view()),
]