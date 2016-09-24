
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from school_log.forms import EntryForm, StudentForm, SubjectForm
from school_log.models import Entry, Student, Subject

## def entries (6 mos)
## def entry-query (custom view from POST)
## def new-entry(requires save_m2m())
## def edit_entry (n)
## def delete_entry
## def confirm_delete_entry (n)

# Entry Views

@login_required
def entries ( request ):

    entries = Entry.objects.filter ( student__user=request.user )
    entries = Paginator ( entries, 50 ).page ( 1 ).object_list
    data = {
        'active_page': 'entries',
        'entries': entries,
        'user': request.user
    }

    return render ( request, 'school-log/entries/list.html', data )

@login_required
def new_entry ( request ):

    if request.method == 'POST':
        form = EntryForm ( data=request.POST )
        if form.is_valid ():
            for student_id in request.POST.get ( 'students' ):

                entry = EntryForm ( data=request.POST ).save ( commit=False )
                # entry = entry.copy ()
                entry.id = None
                entry.pk = None

                student = Student.objects.get ( id=int ( student_id ), user=request.user )
                entry.student = student

                entry.save ()

            return HttpResponseRedirect ( '/school-log/entries' )
    else:
        form = EntryForm ()

    students = Student.objects.filter ( user=request.user )
    data = {
        'active_page': 'entries',
        'form': form,
        'students': students,
        'user': request.user
    }

    return render ( request, 'school-log/entries/new-entry.html', data )

# Student Views

@login_required
def students ( request ):

    students = Student.objects.filter ( user=request.user )
    data = {
        'active_page': 'students',
        'students': students,
        'user': request.user
    }

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
        'form': form,
        'user': request.user
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
        'student': student,
        'user': request.user
    }
    return render ( request, 'school-log/forms/edit-student.html', data )

@login_required
def delete_student ( request, pk ):

    student_id = int ( pk )
    student = Student.objects.get ( id=student_id, user=request.user )

    data = {
        'active_page': 'students',
        'student': student,
        'user': request.user
    }
    return render ( request, 'school-log/forms/delete-student.html', data )

@login_required
def confirm_student_delete ( request, pk ):

    student_id = int ( pk )
    student = Student.objects.get ( id=student_id, user=request.user )

    student.delete ()

    return HttpResponseRedirect ( '/school-log/students' )

@login_required
def subjects ( request ):

    if request.method == 'POST':
        form = SubjectForm ( data=request.POST )
        if form.is_valid ():

            subject = form.save ( commit=False )
            subject.user = request.user
            subject.save ()

            return HttpResponseRedirect ( '/school-log/subjects' )
    else:
        form = SubjectForm ()

    subjects = Subject.objects.filter ( user=request.user )
    data = {
        'active_page': 'subjects',
        'form': form,
        'subjects': subjects,
        'user': request.user
    }

    return render ( request, 'school-log/subjects/get_all.html', data )

@login_required
def delete_subject ( request, pk ):

    subject_id = int ( pk )
    subject = Subject.objects.get ( id=subject_id, user=request.user )

    data = {
        'active_page': 'subjects',
        'subject': subject,
        'user': request.user
    }
    return render ( request, 'school-log/subjects/delete.html', data )

@login_required
def confirm_subject_delete ( request, pk ):

    subject_id = int ( pk )
    subject = Subject.objects.get ( id=subject_id, user=request.user )

    subject.delete ()

    return HttpResponseRedirect ( '/school-log/subjects' )
