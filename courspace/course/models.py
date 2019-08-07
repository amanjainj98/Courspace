## @brief Models for the course app.

from django.db import models
from django.contrib.auth.models import User
from instructor.models import Course
from django.core.urlresolvers import reverse


## @brief This class represents the students enrolled in the website.
class Student(models.Model):
    ## The user associated with the student
    user = models.ForeignKey(User, default=1)

    ## The name of the student
    name = models.CharField(max_length=100)

    ## The roll number the student
    roll_no = models.CharField(max_length=100)

    ## The courses undertaken by the student
    course_list = models.ManyToManyField(Course)

    ## @brief This function returns the string representation of the student class.
    #
    # Used by Django admin website to represent the Student objects.
    # @param self The object pointer.
    def __str__(self):
        return self.name


## @brief This class represents the messages displayed in the forum.
class Message(models.Model):
    ## The content of message
    content = models.CharField(max_length=500)

    ## The course associated with the message
    course = models.ForeignKey(Course,default=1,on_delete=None)

    ## The sender of the message
    sender = models.ForeignKey(User,default=1, on_delete=None)

    ## The time when the message was posted
    time = models.CharField(max_length=100)


## @brief This class represents the notifications receieved by the students.
class Notification(models.Model):
    ## The content of notification
    content = models.CharField(max_length=500)

    ## The course associated with the notification
    course = models.ForeignKey(Course, default=1, on_delete=None)

    ## The time when the notification was posted/generated
    time = models.CharField(max_length=100)


## @brief This class represents the resources(lectures/study materials) for a course.
class Resources(models.Model):
    ## The resource file 
    file_resource = models.FileField(default='')

    ## The title for the resource
    title = models.CharField(max_length=100)

    ## The course associated with the resource
    course = models.ForeignKey(Course, default=1, on_delete=None)


