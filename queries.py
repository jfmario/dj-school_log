
import datetime
from django.db.models import Q
from school_log.models import Entry, Student, Subject

class EntryQuery:

    def __init__ ( self, request ):

        self.user = request.user
        post = request.POST

        self.begin_date = post.get ( 'begin_date',
            '1970-01-01' )
        self.end_date = post.get ( 'end_date',
            '2100-12-31' )
        self.description_keyterms = post.get ( 'description_keyterms', '' ).split ()
        self.hours_min = float ( post.get ( 'hours_min', 0 ) )
        self.hours_max = float ( post.get ( 'hours_max', 9999 ) )
        self.students = [Student.objects.get(id=int(i))for i in post.getlist('students',[])]
        self.subjects = [Subject.objects.get(id=int(i))for i in post.getlist('subjects',[])]

    def execute ( self ):

        query = Entry.objects.filter ( student__user=self.user )
        query = query.filter ( date__gte=self.begin_date, date__lte=self.end_date )
        if self.description_keyterms:
            query = query.filter ( reduce ( lambda x, y: x | y,
                [Q(description__contains=d)for d in self.description] ) )
        query = query.filter ( hours__gte=self.hours_min, hours__lte=self.hours_max )

        if ( self.students ):
            query = query.filter ( student__id__in=self.students )
        if ( self.subjects ):
            query = query.filter ( reduce ( lambda x, y: x | y,
                [Q(subject_id=i)for i in self.subjects] ) )
        return query
