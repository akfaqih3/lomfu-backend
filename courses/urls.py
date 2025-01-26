from django.urls import path
from .views import (
    SubjectViewSet,
    CourseListAPI,
    CourseDetailAPI,
)

urlpatterns= [
    path('subjects/',SubjectViewSet.as_view({'get': 'list'})),
    path('subjects/<slug:slug>/',SubjectViewSet.as_view({'get': 'retrieve'})),

    path('',CourseListAPI.as_view()),
    path('<int:id>/',CourseDetailAPI.as_view()),

]