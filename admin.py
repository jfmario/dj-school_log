from django.contrib import admin
from school_log.models import Entry, Student, Subject, SubjectToEntry

# Register your models here.

class SubjectToEntryInline ( admin.TabularInline ):
    model = SubjectToEntry
    extra = 1

class EntryAdmin ( admin.ModelAdmin ):

    inlines = [SubjectToEntryInline]

    def save_model ( self, request, obj, form, change ):
        obj.author = request.user
        obj.save ()

admin.site.register ( Entry, EntryAdmin )
admin.site.register ( Student )
admin.site.register ( Subject )
