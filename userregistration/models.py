from django.db import models
from django import forms
from enum import Enum
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from .contributor import Contributor

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    email = forms.EmailField(
           label=_("e-mail address"),
           strip=True,
           required=False,
           widget=forms.EmailInput,
           )

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ContributorCreationForm(forms.ModelForm):

    class Meta:
        model = Contributor
        fields = ['sex']

    sex = forms.ChoiceField(
            choices=Contributor.SEX_CHOISES + ((None, 'Please select one'),)
            )
    def save(self, commit=True):
        contributor = super(ContributorCreationForm, self).save(commit=False)
        contributor.sex = self.cleaned_data["sex"]
        if commit:
            contributor.save()
        return contributor


