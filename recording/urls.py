from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^upload',
        views.upload,
        name='upload'),
    url(r'^about',
        views.about,
        name='about'),
    url(r'^getNextSyllable',
        views.get_next_syllable,
        name='get_next_syllable'),
    url(r'^$',
        views.recording,
        name='recording'),
]
