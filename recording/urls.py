from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^upload', views.upload, name='upload'),
        url(r'^introduction', views.introduction, name='intruduction'),
        url(r'^getNextSyllable', views.get_next_syllable, name='get_next_syllable'),
        url(r'^$', views.recording, name='recording'),
        ]
