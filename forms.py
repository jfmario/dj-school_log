
from django.db import models
from django.forms import ModelForm, widgets
from shared.forms import BootstrapModelForm
from school_log.models import Entry, Student, Subject

class EntryForm ( BootstrapModelForm ):

    def __init__ (self, user, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields ['subjects'].queryset = Subject.objects.filter ( user=user )

    class Meta:
        model = Entry
        fields = [ 'date', 'description', 'hours', 'subjects' ]

class EntryFormComplete ( BootstrapModelForm ):

    def __init__(self, user, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
        self.fields ['subjects'].queryset = Subject.objects.filter ( user=user )
        self.fields ['student'].queryset = Student.objects.filter ( user=user )

    class Meta:
        model = Entry
        fields = [ 'date', 'description', 'hours', 'student', 'subjects' ]

class StudentForm ( BootstrapModelForm ):
    class Meta:
        model = Student
        fields = [ 'name', 'age', 'grade' ]

class SubjectForm ( BootstrapModelForm ):
    class Meta:
        model = Subject
        fields = ['name']
