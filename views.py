
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from school_log.forms import StudentForm
from school_log.models import Student

## def entries (6 mos)
## def entry-query (custom view from POST)
## def new-entry(requires save_m2m())
## def edit_entry (n)
## def delete_entry
## def confirm_delete_entry (n)

# Student Views

@login_required
def students ( request ):

    students = Student.objects.filter ( user=request.user )
    data = { 'students': students }

    data ['active_page'] = 'students'
    return render ( request, 'school-log/students.html', data )

@login_required
def new_student ( request ):

    if request.method == 'POST':
        form = StudentForm ( data=request.POST )
        if form.is_valid ():

            student = form.save ( commit=False )
            student.user = request.user
            student.save ()

            return HttpResponseRedirect ( '/school-log/students' )
    else:
        form = StudentForm ()

    data = {
        'active_page': 'students',
        'form': form
    }
    return render ( request, 'school-log/forms/new-student.html', data )

@login_required
def edit_student ( request, pk ):

    student_id = int ( pk )
    student = Student.objects.get ( id=student_id, user=request.user )

    if request.method == 'POST':
        form = StudentForm ( data=request.POST, instance=student )
        if form.is_valid ():

            student = form.save ( commit=False )
            student.user = request.user
            student.save ()

            return HttpResponseRedirect ( '/school-log/students' )

    else:
        form = StudentForm ( instance=student )

    data = {
        'active_page': 'students',
        'form': form,
        'student': student
    }
    return render ( request, 'school-log/forms/edit-student.html', data )

def delete_student ( request, pk ):

    student_id = int ( pk )
    student = Student.objects.get ( id=student_id, user=request.user )

    data = {
        'active_page': students,
        'student': student
    }
    return render ( request, 'school-log/forms/delete-student.html', data )

def confirm_student_delete ( request, pk ):

    student_id = int ( pk )
    student = Student.objects.get ( id=student_id, user=request.user )

    student.delete ()

    return HttpResponseRedirect ( '/school-log/students' )

# def subjects (list and optional add 1 at a time)
