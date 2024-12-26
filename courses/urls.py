from django.urls import path
from .views import (
    SubjectViewSet,
)

urlpatterns= [
    path('subjects/',SubjectViewSet.as_view({'get': 'list'})),
    path('subjects/<slug:slug>/',SubjectViewSet.as_view({'get': 'retrieve'})),
]