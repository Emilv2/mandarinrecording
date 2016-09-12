from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
        url(r'^registration/', views.registration, name='registration'),
        url(r'^login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
        url(r'^password_reset/', views.password_reset, name='password_reset'),
        ]
