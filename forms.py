
from django.db import models
from django.forms import ModelForm, widgets
from school_log.models import Entry, Student, Subject

class EntryForm ( ModelForm ):
    '''
    def __init__ ( self, user, *args, **kwargs ):
        super ( EntryForm, self ).__init__ ( *args, **kwargs )
        # self.fields ['student'] = Student.objects.filter ( user=user )
        self.fields ['subjects'] = Subject.objects.filter ( user=user )
    '''
    class Meta:
        model = Entry
        fields = [ 'date', 'description', 'hours', 'subjects' ]
        widgets = {
            'date': widgets.DateInput ( attrs= { 'class': 'form-control' } ),
            'description': widgets.Textarea ( attrs= { 'class': 'form-control' } ),
            'hours': widgets.NumberInput ( attrs= { 'class': 'form-control' } ),
            'subjects': widgets.Select ( attrs= { 'class': 'form-control' } ),
        }

class EntryFormComplete ( ModelForm ):
    class Meta:
        model = Entry
        fields = [ 'date', 'description', 'hours', 'student', 'subjects' ]

class StudentForm ( ModelForm ):
    class Meta:
        model = Student
        fields = [ 'name', 'age', 'grade' ]

class SubjectForm ( ModelForm ):
    class Meta:
        model = Subject
        fields = ['name']
