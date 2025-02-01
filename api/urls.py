from django.urls import path, include



urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('teachers/', include('teachers.urls')),
    path('courses/', include('courses.urls')),
    path('students/', include('students.urls')),

]