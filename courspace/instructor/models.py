## @brief Models for the instructor app.

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


## @brief This class represents the instructors enrolled in the website.
class Instructor(models.Model):
    ## The user associated with the instructor
    user = models.ForeignKey(User, default=1)

    ## The name of the instructor
    name = models.CharField(max_length=100)

    ## The information about the instructor
    information = models.CharField(max_length=1000,default=1)

    ## @brief This function returns the string representation of the instructor class.
    #
    # Used by Django admin website to represent the instructor objects.
    # @param self The object pointer.
    def __str__(self):
        return self.name


## @brief This class represents the courses.
class Course(models.Model):
    ## The name of the course
    name = models.CharField(max_length=100)

    ## The course code
    code = models.CharField(max_length=100)

    ## The instructor of the course
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    ## The course logo
    course_logo = models.FileField(default=1)

    ## @brief This function returns the string representation of the course class.
    #
    # Used by Django admin website to represent the course objects.
    def __str__(self):
        return self.name


## @brief This class represents the assignments in a course.
class Assignment(models.Model):
    ## The description of the assignment
    description = models.CharField(max_length=1000, default='')

    ## The file containing the problems for the assignment
    file = models.FileField(default='')

    ## The course associated with the assignment
    course = models.ForeignKey(Course)

    ## The date,time of posting the assignment
    post_time = models.CharField(max_length=100)

    ## The deadline to complete the assignment for the students
    deadline = models.CharField(max_length=100)


## @brief This class represents the submissions for an assignment.
class Submission(models.Model):
    ## The file submitted by student
    file_submitted = models.FileField(default='')

    ## The date,time of uploading the submission
    time_submitted = models.CharField(max_length=100)

    ## The user associated with the submission(who uploaded the submission)
    user = models.ForeignKey(User, default=1)

    ## The assignment associated with the submission
    assignment = models.ForeignKey(Assignment, default=1)

    ## @var The list of integer choices available to give feedback for the assignment for which the submission is uploaded
    CHOICES = [(i+1, i+1) for i in range(10)]

    ## The feedback given to the assignment by the student while uploading the submission
    feedback = models.IntegerField(choices=CHOICES)




