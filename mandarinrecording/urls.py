"""mandarinrecording URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from reset_password.views import ResetPasswordRequestView, PasswordResetConfirmView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^reset_password/', include('reset_password.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^recording/', include('recording.urls')),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('about'))),
]
