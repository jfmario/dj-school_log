
from django.db import models
from django.forms import ModelForm
from school_log.models import Entry, Student, Subject

class EntryForm ( ModelForm ):

    def __init__ ( self, user, *args, **kwargs ):
        super ( EntryForm, self ).__init__ ( *args, **kwargs )
        # self.fields ['student'] = Student.objects.filter ( user=user )
        self.fields ['subjects'] = Subject.objects.filter ( user=user )

    class Meta:
        model = Entry
        fields = [ 'date', 'description', 'hours', 'subjects' ]

class StudentForm ( ModelForm ):
    class Meta:
        model = Student
        fields = [ 'name', 'age', 'grade' ]

class SubjectForm ( ModelForm ):
    class Meta:
        model = Subject
        fields = ['name']
