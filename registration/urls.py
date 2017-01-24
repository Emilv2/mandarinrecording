from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [url(r'^registration/',
                   views.registration,
                   name='registration'),
               url(r'^login/',
                   views.login,
                   {'template_name': 'login.html'},
                   name='login'),
               url(r'^logout/',
                   auth_views.logout,
                   {'next_page': '/accounts/login'},
                   name='logout'),
               ]
