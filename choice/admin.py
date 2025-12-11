from django.contrib import admin

# Register your models here.
from .models import Course,Lesson,Courses
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Courses)
