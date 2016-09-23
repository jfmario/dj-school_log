
from django.conf.urls import url
from school_log.views import students, new_student, edit_student, delete_student

URLS = [
    url ( r'^$', students ),
    url ( r'students/', students ),
    url ( r'new-student/', new_student ),
    url ( r'edit-student/(?P<pk>[0-9]+)/$', edit_student ),
    url ( r'delete-student/(?P<pk>[0-9]+)/$', delete_student )
]
