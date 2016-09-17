from django.db import models
from django import forms
from enum import Enum
from os import walk
import random
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.html import format_html
from .contributor import Contributor

AUDIO_DIR = 'userregistration/static'

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    username = forms.EmailField(
            label=_("e-mail address"),
            strip=True,
            required=False,
            widget=forms.EmailInput,
            )


    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user

class ContributorCreationForm(forms.ModelForm):

    class Meta:
        model = Contributor
        fields = ['sex', 'accepted_licence']

    sex = forms.ChoiceField(
            choices=Contributor.SEX_CHOISES + ((None, 'Please select one'),)
            )

    accepted_licence = forms.BooleanField(
            label=_(format_html("I accept that my contributions are released under the \
                    <a href='https://creativecommons.org/licenses/by-sa/4.0/'> \
                Creative Commons CC BY-SA 4.0 license</a>.")),
            required=True
            )


    def save(self, commit=True):
        contributor = super(ContributorCreationForm, self).save(commit=False)
        contributor.sex = self.cleaned_data["sex"]
        contributor.syllables_list = create_base_syllables_list()
        if commit:
            contributor.save()
        return contributor

# PINYIN_LIST = ['ai1','ai2','ai3','ai4','ai5',
#         'ma1','ma2','ma3','ma4','ma5',
#         'ma1','ma2','ma3','ma4','ma5',
#         'ma1','ma2','ma3','ma4','ma5',
#         'ma1','ma2','ma3','ma4','ma5',
#         'wo1','wo2','wo3','wo4','wo5',
#         ]
PINYIN_LIST = ['ai1']

def read_file():
    """
    return a random filename from the audio directory
    """
    _, _, filenames = next(walk(AUDIO_DIR))
    return random.choice(filenames)

class AudioCaptchaForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AudioCaptchaForm, self).__init__(*args, **kwargs)
        self.audio_file = read_file()

    pinyin = forms.CharField()

    def is_valid(self):
        is_valid = super(AudioCaptchaForm, self).is_valid()
        if not is_valid:
            return False
        else:
            pinyin = self.cleaned_data['pinyin']\
                    .replace('0','5')\
                    .replace(' ','')
            if pinyin == PINYIN_LIST[int(self.audio_file.split('.')[0])]:
                return True
            else:
                return False

def create_base_syllables_list():
    with open('syllables_without_tones_short_list','r') as text_file:
        syllables = [line.strip('\n') for line in text_file.readlines()]
        selection1 = random.sample(syllables,4)
        selection2 = [random.choice(syllables) for i in range(4)]
        sound_list= ''
        for i in range(4):
            for j in range(1,6):
                sound_list += selection1[i]+str(j)+';'
        for i in range(2):
            for j in range(1,5):
                for k in range(1,6):
                    sound_list += selection2[i]+str(j)+"_"+selection2[i+1]+str(k)+';'
        return sound_list
