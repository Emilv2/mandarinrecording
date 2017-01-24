from django.contrib import admin
#from views import ResetPasswordRequestView, PasswordResetConfirmView
from . import views

from django.conf.urls import include, url

urlpatterns = [
    url(r'^confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        views.PasswordResetConfirmView.as_view(),
        name='reset_password_confirm'),
    # PS: url above is going to used for next section of
    # implementation.
    url(r'^reset/',
        views.ResetPasswordRequestView.as_view(),
        name="reset_password"),
    ]
