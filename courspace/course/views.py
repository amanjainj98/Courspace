## @brief Views for the course app.

from django.contrib.auth.decorators import login_required
from .models import Student, Message, Notification, Resources
from instructor.models import Assignment, Course, Instructor
from django.shortcuts import render, redirect
from .forms import MessageForm, SubmissionForm
import datetime


## @brief view for the index page of the student.
#
# This view is called by /index url.\n
# It returns the student's homepage containing links to all the courses he is enrolled in and all the notifications.
@login_required
def index(request):
    student = Student.objects.get(user=request.user)
    courses = student.course_list.all()
    notifications = Notification.objects.filter(course__in=courses)
    return render(request, 'course/index.html', {'courses': courses, 'notifications': notifications})


## @brief view for the detail page of the course.
#
# This view is called by <course_id>/detail url.\n
# It returns the course's detail page containing forum and links to all the assignments and resources.
@login_required
def detail(request, course_id):
    user = request.user
    student = Student.objects.get(user=request.user)
    courses = student.course_list.all()
    course = Course.objects.get(id=course_id)
    instructor = course.instructor
    messages = Message.objects.filter(course=course)
    form = MessageForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.course = course
            message.sender = user
            message.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y') # get the current date,time and convert into string
            message.save()
            try:
                student = Student.objects.get(user=request.user)
                return redirect('course:detail', course_id)

            except:
                return redirect('instructor:instructor_detail', course.id)

    else:
        form = MessageForm()

        context = {
            'course': course,
            'user': user,
            'instructor': instructor,
            'student': student,
            'courses': courses,
            'messages': messages,
            'form': form
        }

        return render(request, 'course/detail.html', context)


## @brief view for the assignments page of a course.
#
# This view is called by <course_id>/view_assignments url.\n
# It returns the webpage containing all the assignments of the course and links to download them and upload submissions.
@login_required
def view_assignments(request, course_id):
    course = Course.objects.get(id=course_id)
    assignments = Assignment.objects.filter(course=course)
    context = {
        'course' : course,
        'assignments' : assignments,
    }
    return render(request,'course/view_assignments.html',context)


## @brief view for the resources page of a course.
#
# This view is called by <course_id>/view_resources url.\n
# It returns the webpage containing all the resources of the course and links to download them.
@login_required
def view_resources(request, course_id):
    course = Course.objects.get(id=course_id)
    resources = Resources.objects.filter(course=course)
    context = {
        'course' : course,
        'resources' : resources,
    }
    return render(request,'course/view_resources.html',context)


## @brief view for the assignment's submission page.
#
# This view is called by <assignment_id>/upload_submission url.\n
# It returns the webpage containing a form to upload submission and redirects to the assignments page again after the form is submitted.
@login_required
def upload_submission(request, assignment_id):
    form = SubmissionForm(request.POST or None, request.FILES or None)
    assignment = Assignment.objects.get(id=assignment_id)
    course_id = assignment.course.id
    course = Course.objects.get(id=course_id)
    if form.is_valid():
        submission = form.save(commit=False)
        submission.user = request.user
        submission.assignment = assignment
        submission.time_submitted = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
        submission.save()
        return view_assignments(request, course_id)

    return render(request, 'course/upload_submission.html', {'form': form,'course': course})


