## @brief The models registered for the admin site

from django.contrib import admin
from .models import Student, Message, Notification, Resources


admin.site.register(Student)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Resources)