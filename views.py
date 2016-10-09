
import csv, datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from school_log.forms import EntryForm, EntryFormComplete, StudentForm, SubjectForm
from school_log.models import Entry, Student, Subject, SubjectToEntry
from school_log.queries import EntryQuery

width, height = A4

def coord(x, y, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

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
        form = EntryForm ( data=request.POST, user=request.user )
        print ( '[SCHOOL-LOG] views.new_entry: request.POST =>', request.POST )
        for student_id in request.POST.getlist ( 'students' ):

            print ( '[SCHOOL-LOG] views.new_entry: for(student_id)', student_id )

            new_entry = Entry ( date=datetime.datetime.strptime ( request.POST.get ( 'date' ), '%Y-%m-%d' ),
                description=request.POST.get ( 'description' ),
                hours=float( request.POST.get ( 'hours' ) ) )
            student = Student.objects.get ( id=int ( student_id ), user=request.user )

            new_entry.student = student
            print ( '[SCHOOL-LOG] views.new_entry: for(student_id) new_entry =>', new_entry, new_entry.id )
            new_entry.save ()
            print ( '[SCHOOL-LOG] views.new_entry: for(student_id) new_entry =>', new_entry )

            for subject in request.POST.getlist ( 'subjects' ):
                se = SubjectToEntry ( subject=Subject.objects.get ( id=int(subject) ),
                    entry=new_entry )
                se.save ()
                se = None

            new_entry = None

        return HttpResponseRedirect ( '/school-log/entries' )
    else:
        form = EntryForm ( user=request.user )

    students = Student.objects.filter ( user=request.user )
    data = {
        'active_page': 'entries',
        'form': form,
        'students': students,
        'user': request.user
    }

    return render ( request, 'school-log/entries/new-entry.html', data )

@login_required
def edit_entry ( request, pk ):

    entry_id = int ( pk )
    entry = Entry.objects.get ( id=entry_id, student__user=request.user )

    if request.method == 'POST':
        form = EntryFormComplete ( data=request.POST, user=request.user, instance=entry )
        if form.is_valid ():

            entry = form.save ( commit=False )
            entry.user = request.user
            entry.save ()
            SubjectToEntry.objects.filter ( entry=entry ).delete ()

            for subject_id in request.POST.getlist ( 'subjects' ):
                se = SubjectToEntry ( subject=Subject.objects.get ( id=int(subject_id) ),
                    entry=entry )
                se.save ()

            return HttpResponseRedirect ( '/school-log/entries' )

    else:
        form = EntryFormComplete ( instance=entry, user=request.user )

    data = {
        'active_page': 'entries',
        'form': form,
        'entry': entry,
        'user': request.user
    }
    return render ( request, 'school-log/entries/edit.html', data )

@login_required
def query_entries ( request ):

    data = {
        'active_page': 'entries',
        'user': request.user
    }

    if request.method == 'POST':

        output_format = request.POST.get ( 'format' )
        query_object = EntryQuery ( request )

        entries = query_object.execute ()

        if output_format == 'CSV':

            response = HttpResponse ( content_type='text/csv' )
            response ['Content-Disposition'] = 'attachment;filename="school-log.csv"'
            writer = csv.writer ( response )

            writer.writerow ( [ 'Date', 'Student', 'Subjects', 'Hours',
                'Description' ] )

            for entry in entries:
                cells = [
                    entry.get_date (),
                    entry.student.name,
                    entry.get_subject_list (),
                    str ( entry.hours ),
                    entry.description
                ]
                writer.writerow ( cells )

            return response
        elif output_format == 'PDF':

            response = HttpResponse ( content_type='application/pdf' )
            response ['Content-Disposition'] = 'attachment;filename="school-log.pdf"'
            p = canvas.Canvas ( response )

            table_data = [ [ 'Date', 'Student', 'Subjects', 'Hours',
                'Description' ] ]

            for entry in entries:
                table_data.append ([
                    entry.get_date (),
                    entry.student.name,
                    entry.get_subject_list (),
                    str ( entry.hours ),
                    entry.description
                ])

            t = Table ( table_data )
            t.setStyle ( TableStyle ([
                ( 'BACKGROUND', (0,0), (4,0), colors.gray )
            ]))
            t.wrapOn(p, width, height)
            t.drawOn(p, *coord(1.8, 9.6, cm))

            p.showPage ()
            p.save ()

            return response
        else:
            data ['entries'] = query_object.execute ()
            return render ( request, 'school-log/entries/list.html', data )
    else:
        data ['students'] = Student.objects.filter ( user=request.user )
        data ['subjects'] = Subject.objects.filter ( user=request.user )
        return render ( request, 'school-log/entries/query.html', data )

@login_required
def delete_entry ( request, pk ):

    entry_id = int ( pk )
    entry = Entry.objects.get ( id=entry_id, student__user=request.user )

    data = {
        'active_page': 'entries',
        'entry': entry,
        'user': request.user
    }
    return render ( request, 'school-log/entries/delete.html', data )

@login_required
def confirm_entry_delete ( request, pk ):

    entry_id = int ( pk )
    entry = Entry.objects.get ( id=entry_id, student__user=request.user )

    entry.delete ()

    return HttpResponseRedirect ( '/school-log/entries' )

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

def about ( request ):
    return TemplateResponse ( request, 'school-log/about.html', {} )
