
from django.conf.urls import url
from school_log.views import *

URLS = [

    url ( r'^$', students ),

    # entry views
    url ( r'entries/', entries ),
    url ( r'new-entry/', new_entry ),

    # student views
    url ( r'students/', students ),
    url ( r'new-student/', new_student ),
    url ( r'edit-student/(?P<pk>[0-9]+)/$', edit_student ),
    url ( r'delete-student/(?P<pk>[0-9]+)/$', delete_student ),
    url ( r'confirm-student-delete/(?P<pk>[0-9]+)/$', confirm_student_delete ),

    # subject views
    url ( r'subjects/', subjects ),
    url ( r'delete-subject/(?P<pk>[0-9]+)/$', delete_subject ),
    url ( r'confirm-subject-delete/(?P<pk>[0-9]+)/$', confirm_subject_delete )
]
