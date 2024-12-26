from django.contrib import admin
from .models import (
    Subject,
    Course,
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'total_courses')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created',  'photo')
    search_fields = ('title',)
