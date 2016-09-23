
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from school_log.forms import StudentForm
from school_log.models import Student

## def entries (6 mos)
## def entry-query (custom view from POST)
## def new-entry
## def edit_entry (n)
## def delete_entry
## def confirm_delete_entry (n)

# Student Views

@login_required
def students ( request ):

    students = Student.objects.filter ( user=request.user )
    data = { 'students': students }

    data ['active'] = 'students'
    return render ( request, 'school-log/students.html', data )

@login_required
def new_student ( request ):

    if request.method == 'POST':
        form = StudentForm ( request, user=request.user )
        if form.is_valid ():

            form.save ()

            return HttpResponseRedirect ( '/school-log/students' )
    else:
        form = StudentForm ( request, user=request.user )

    data = {
        'active': 'students'
        'form': form
    }
    return render ( request, 'school-log/forms/new-student.html', data )

## edit_student (n)
## delete_students
## confirm_delete_student (n)

# def subjects (list and optional add 1 at a time)
