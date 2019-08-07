## @brief Forms for the course app.

from django import forms
from django.contrib.auth.models import User
from course.models import Student

## @brief This class represents the form to register a user.
class UserRegistration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


## @brief This class represents the form to register a student.
class StudentRegistration(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'course_list']


