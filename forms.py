
from django.db import models
from django.forms import ModelForm, widgets
from school_log.models import Entry, Student, Subject

class EntryForm ( ModelForm ):

    def __init__(self, user, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
        self.fields ['subjects'] = Subject.objects.filter ( user=user )

    class Meta:
        model = Entry
        fields = [ 'date', 'description', 'hours', 'subjects' ]

class EntryFormComplete ( ModelForm ):

    def __init__(self, user, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
        self.fields ['subjects'] = Subject.objects.filter ( user=user )
        self.fields ['students'] = Student.objects.filter ( user=user )

    class Meta:
        model = Entry
        fields = [ 'date', 'description', 'hours', 'student', 'subjects' ]

class StudentForm ( ModelForm ):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    class Meta:
        model = Student
        fields = [ 'name', 'age', 'grade' ]

class SubjectForm ( ModelForm ):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    class Meta:
        model = Subject
        fields = ['name']
