
from django.contrib.auth.models import User
from django.db import models

class Entry ( models.Model ):

    date = models.DateField ( default=date.today )
    description = models.TextField ( blank=True, null=True )
    hours = models.FloatField ( default=1 )
    student = models.ForeignKey ( Student )
    subjects = models.ManyToManyField ( Subject, blank=True, null=True, through="SubjectToEntry" )

    class Meta:
        ordering = ['date']

    def __str__ ( self ):
        return self.date.strftime ( '%Y/%m/%d' ) + ' -> ' + self.student.name + ' (' + self.hours + ' hrs. )'

class Student ( models.Model ):

    GRADE_CHOICES = [ 'Pre', 'K' ] + [str(i)for i in range(1,13)] + ['Other']

    age = models.PositiveIntegerField ( default=0 )
    grade = models.CharField ( choices=GRADE_CHOICES, default='1', max_length=8 )
    name = models.CharField ( max_length=64 )
    user = models.ForeignKey ( user )

    class Meta:
        ordering = ['-age','name']

    def __str__ ( self ):
        return self.name

class Subject ( models.Model ):

    name = models.CharField ( max_length=128 )
    user = models.ForeignKey ( user )

    class Meta:
        ordering = ['name']

    def __str__ ( self ):
        return self.name

class SubjectToEntry ( models.Model ):
    entry = models.ForeignKey ( Entry )
    subject = models.ForeignKey ( Subject )
