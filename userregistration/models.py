from django.db import models
from django import forms
from enum import Enum
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _

class Contributor(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    NO_ANSWER = 'N'
    SEX_CHOISES = (
            (MALE, 'Male'),
            (FEMALE, 'Female'),
            (NO_ANSWER, 'No_answer'),
            )
    sex = models.CharField(
            max_length=2,
            choices=SEX_CHOISES,
            )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    registration_date = models.DateTimeField()
    email = models.EmailField()

class ContributorCreationForm(UserCreationForm):
    email = forms.EmailField(
            label=_("e-mail address"),
            strip=True,
            required=False,
            widget=forms.EmailInput,
            )
