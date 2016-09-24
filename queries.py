
import datetime
from school_log.models import Student, Subject

class EntryQuery:
    def __init__ ( self, post ):
        self.begin_date = datetime.datetime.striptime ( post.get ( 'begin_date',
            '1970-01-01' ), '%Y-%m-%m' )
        self.end_date = datetime.datetime.striptime ( post.get ( 'end_date',
            '2100-12-31' ), '%Y-%m-%m' )
        self.description_keyterms = post.get ( 'description_keyterms', '' ).split ()
        self.hours_min = float ( post.get ( 'hours_min', 0 ) )
        self.hours_max = float ( post.get ( 'hours_max', 9999 ) )
        self.students = [Student.objects.get(id=int(i))for i in post.getlist('students',[])]
        self.subjects = [Subject.objects.get(id=int(i))for i in post.getlist('subjects',[])]
