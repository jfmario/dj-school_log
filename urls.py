
from django.conf.urls import url
from school_log.views import students

URLS = [
    url ( r'^$', students ),
    url ( r'students/', students )
]
