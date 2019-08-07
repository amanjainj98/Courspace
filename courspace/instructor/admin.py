## @brief The models registered for the admin site

from django.contrib import admin
from .models import Instructor, Course, Assignment, Submission


admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Submission)