## @brief Views for the instructor app.

from django.contrib.auth.decorators import login_required
from .models import Instructor, Submission, Assignment
from course.models import Course, Message, Notification, Student
from django.shortcuts import render, HttpResponse, redirect
from .forms import AssignmentForm, NotificationForm, ResourceForm
from course.forms import MessageForm
import datetime


## @brief view for the index page of the instructor.
#
# This view is called by /instructor_index url.\n
# It returns the instructor's homepage containing links to all the courses he teaches.
@login_required
def instructor_index(request):
    user = request.user
    instructor = Instructor.objects.get(user=request.user)
    courses = Course.objects.filter(instructor=instructor)
    context = {
        'user': user,
        'instructor': instructor,
        'courses': courses,
    }
    return render(request, 'instructor/instructor_index.html', context)


## @brief view for the detail page of the course.
#
# This view is called by <course_id>/instructor_detail url.\n
# It returns the course's detail page containing forum and links to add assignment,resource,notifications
# and view all the assignments and their submissions.
@login_required
def instructor_detail(request, course_id):
    user = request.user
    instructor = Instructor.objects.get(user=request.user)
    courses = Course.objects.filter(instructor=instructor)
    course = Course.objects.get(id=course_id)
    messages = Message.objects.filter(course=course)
    form = MessageForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.course = course
            message.sender = user
            message.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
            message.save()
            try:
                student = Student.objects.get(user=request.user)
                return redirect('course:detail', course_id)

            except:
                return redirect('instructor:instructor_detail', course.id)

    else:
        form = MessageForm()

        context = {
                'user': user,
                'instructor': instructor,
                'course': course,
                'courses': courses,
                'messages': messages,
                'form' : form
            }

        return render(request, 'instructor/instructor_detail.html', context)


## @brief view for the course's add-notification page
#
# This view is called by <course_id>/add_notification url.\n
# It returns the webpage containing a form to add notification and redirects to the course's detail page again after the form is submitted.
@login_required
def add_notification(request, course_id):
    form = NotificationForm(request.POST or None)
    course = Course.objects.get(id=course_id)
    if form.is_valid():
        notification = form.save(commit=False)
        notification.course = course
        notification.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y') # get the current date,time and convert into string
        notification.save()
        return redirect('instructor:instructor_detail', course.id)

    return render(request, 'instructor/add_notification.html', {'course': course, 'form': form})


## @brief view for the course's add-assignment page.
#
# This view is called by <course_id>/add_assignment url.\n
# It returns the webpage containing a form to add an assignment and redirects to the course's detail page again after the form is submitted.
@login_required
def add_assignment(request, course_id):
    form = AssignmentForm(request.POST or None, request.FILES or None)
    course = Course.objects.get(id=course_id)
    if form.is_valid():
        assignment = form.save(commit=False)
        assignment.file = request.FILES['file']
        assignment.post_time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
        assignment.course = course
        assignment.save()
        notification = Notification()
        notification.content = "New Assignment Uploaded"
        notification.course = course
        notification.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
        notification.save()
        return redirect('instructor:instructor_detail', course.id)

    return render(request, 'instructor/create_assignment.html', {'form': form, 'course': course})


## @brief view for the course's add-resource page.
#
# This view is called by <course_id>/add_resource url.\n
# It returns the webpage containing a form to add a resource and redirects to the course's detail page again after the form is submitted.
@login_required
def add_resource(request, course_id):
    form = ResourceForm(request.POST or None, request.FILES or None)
    instructor = Instructor.objects.get(user=request.user)
    course = Course.objects.get(id=course_id)
    if form.is_valid():
        resource = form.save(commit=False)
        resource.file_resource = request.FILES['file_resource']
        resource.course = course
        resource.save()
        notification = Notification()
        notification.content = "New Resource Added - " + resource.title
        notification.course = course
        notification.time = datetime.datetime.now().strftime('%H:%M, %d/%m/%y')
        notification.save()
        return redirect('instructor:instructor_detail', course.id)

    return render(request, 'instructor/add_resource.html', {'form': form, 'course': course})


## @brief view for the assignments page of a course.
#
# This view is called by <course_id>/view_all_assignments url.\n
# It returns the webpage containing all the assignments of the course and links to their submissions and feedbacks given by the students.
@login_required
def view_all_assignments(request, course_id):
    course = Course.objects.get(id=course_id)
    assignments = Assignment.objects.filter(course=course)
    return render(request, 'instructor/view_all_assignments.html', {'assignments' : assignments,'course': course})


## @brief view for the submissions page of an assignment.
#
# This view is called by <assignment_id>/view_all_submissions url.\n
# It returns the webpage containing links to all the submissions of an assignment.
@login_required
def view_all_submissions(request,assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    course = assignment.course
    return render(request, 'instructor/view_all_submissions.html', {'submissions' : submissions,'course': course})


## @brief view for the feedback page containing an histogram of all the feddbacks provided by the students.
#
# This view is called by <assignment_id>/view_feedback url.\n
# It returns a webpage containing the feedback received by the students organized in the form of histogram.
@login_required
def view_feedback(request,assignment_id):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    import matplotlib.ticker as ticker

    assignment = Assignment.objects.get(id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)

    feedbacks1 = list(map(lambda x: x.feedback, submissions)) #extract the feedbacks from the submissions list
    feedbacks = np.array(feedbacks1)

    fig = plt.figure(figsize=(10,6))
    fig.suptitle('Feedback received from the students', fontsize=16, fontweight='bold')
    fig.subplots_adjust(bottom=0.3)
    ax = fig.add_subplot(111)

    ax.set_xlabel('Rating(out of 10)')
    ax.set_ylabel('Number of Students')
    x = feedbacks
    ax.hist(x, bins=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], fc='lightblue', alpha=1, align='left', edgecolor='black', linewidth=1.0)
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1)) #sets the difference between adjacent y-tics

    plt.figtext(0.2, 0.1, 'Average Rating : '+ str(round(np.mean(feedbacks),2)),
                bbox={'facecolor': 'lightblue', 'alpha': 0.5, 'pad': 10})     #adds box in graph to display mean rating
    plt.figtext(0.5, 0.1, 'Number of Students Students who rated : ' + str(len(feedbacks1)),
                bbox={'facecolor': 'lightblue', 'alpha': 0.5, 'pad': 10})     #adds box in graph to display number of students who rated

    canvas = FigureCanvasAgg(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)  # converts the figure to http response
    return response