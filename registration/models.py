from django import forms
from os import walk
import random
import re
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from .contributor import Contributor
from django.conf import settings
from django.core.exceptions import ValidationError

HELP_TEXT = _('Used for attribution, can be an alias, if left blank e-mail will be used for attribution.')


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
            max_length=30,
            label=_('First Name (optional)'),
            help_text=HELP_TEXT,
            required=False,
            )
    last_name = forms.CharField(
            max_length=30,
            label=_('Last Name (optional)'),
            help_text=HELP_TEXT,
            required=False,
            )


    username = forms.EmailField(
        label=_("e-mail address"),
        strip=True,
        widget=forms.EmailInput,
    )

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class ContributorCreationForm(forms.ModelForm):

    class Meta:
        model = Contributor
        fields = ['sex', 'accepted_license']

    sex = forms.ChoiceField(
        choices=Contributor.SEX_CHOISES + ((None, _('I am...')),)
    )

    accepted_license = forms.BooleanField(
        label=_(format_html(
                "I accept that my contributions are released under the \
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

PINYIN_DICT = {'pinyin1':'ai1',
               'pinyin2':'wo4',
               'pinyin3':'ma2',
              }

class AudioCaptchaForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AudioCaptchaForm, self).__init__(*args, **kwargs)

    pinyin1 = forms.CharField()
    pinyin2 = forms.CharField()
    pinyin3 = forms.CharField()

    def is_valid_pinyin(self, pinyin):
        data = self.data[pinyin]\
            .replace('0', '5')\
            .replace(' ', '')
        if data == PINYIN_DICT[pinyin]:
            return True
        else:
            return False

    def is_valid(self):
        is_valid = super(AudioCaptchaForm, self).is_valid()
        if not is_valid:
            return False
        else:
            return self.is_valid_pinyin('pinyin1')\
                    and self.is_valid_pinyin('pinyin2')\
                    and self.is_valid_pinyin('pinyin3')

    def clean_pinyin(self, pinyin):
        if self.is_valid_pinyin(pinyin):
            return pinyin
        else:
            raise ValidationError(
                _('Wrong pinyin, please try again.'
                  ' Tones must be included (i.e., write ma1 if you hear 妈,'
                  ' ma5 if you hear 吗).'),
                code='invalid_pinyin')

    def clean_pinyin1(self):
        return self.clean_pinyin('pinyin1')

    def clean_pinyin2(self):
        return self.clean_pinyin('pinyin2')

    def clean_pinyin3(self):
        return self.clean_pinyin('pinyin3')

def create_base_syllables_list():
    with open('registration/syllables_without_tones_short_list', 'r') as text_file:
        syllables = [line.strip('\n') for line in text_file.readlines()]
        selection1 = random.sample(syllables, 4)
        selection2 = [random.choice(syllables) for i in range(4)]
        sound_list = ''
        for i in range(4):
            for j in range(1, 6):
                sound_list += selection1[i] + str(j) + ';'
        for i in range(2):
            for j in range(1, 5):
                for k in range(1, 6):
                    sound_list += selection2[i] + \
                        str(j) + "_" + selection2[i + 1] + str(k) + ';'
        return sound_list


def get_random_syllables():
    with open('registration/syllables_with_tones', 'r') as text_file:
        syllables = [line.strip('\n') for line in text_file.readlines()]
        length = random.randint(1, 4)
        while True:
            selection = random.choice(syllables)
            if selection[-1] != '5':
                break
        for i in range(length - 1):
            selection += '_' + random.choice(syllables)
        return selection


def pretty_pinyin(string):
    replacements = {
        'a1': 'ā', 'a2': 'á', 'a3': 'ǎ', 'a4': 'à', 'a5': 'a', 'e1': 'ē',
        'e2': 'é', 'e3': 'ě', 'e4': 'è', 'e5': 'e', 'i1': 'ī', 'i2': 'í',
        'i3': 'ǐ', 'i4': 'ì', 'i5': 'i', 'o1': 'ō', 'o2': 'ó', 'o3': 'ǒ',
        'o4': 'ò', 'o5': 'o', 'u1': 'ū', 'u2': 'ú', 'u3': 'ǔ', 'u4': 'ù',
        'u5': 'u', 'v1': 'ǖ', 'v2': 'ǘ', 'v3': 'ǚ', 'v4': 'ǜ', 'v5': 'ü',
        'ai1': 'āi', 'ai2': 'ái', 'ai3': 'ǎi', 'ai4': 'ài', 'ai5': 'ai',
        'ei1': 'ēi', 'ei2': 'éi', 'ei3': 'ěi', 'ei4': 'èi', 'ei5': 'ei',
        'ao1': 'āo', 'ao2': 'áo', 'ao3': 'ǎo', 'ao4': 'ào', 'ao5': 'ao',
        'ou1': 'ōu', 'ou2': 'óu', 'ou3': 'ǒu', 'ou4': 'òu', 'ou5': 'ou5',
        'an1': 'ān', 'an2': 'án', 'an3': 'ǎn', 'an4': 'àn', 'an5': 'an',
        'en1': 'ēn', 'en2': 'én', 'en3': 'ěn', 'en4': 'èn', 'en5': 'en',
        'ang1': 'āng', 'ang2': 'áng', 'ang3': 'ǎng', 'ang4': 'àng',
        'ang5': 'ang', 'eng1': 'ēng', 'eng2': 'éng', 'eng3': 'ěng',
        'eng4': 'èng', 'eng5': 'eng', 'ong1': 'ōng', 'ong2': 'óng',
        'ong3': 'ǒng', 'ong4': 'òng', 'ong5': 'ong', 'ia1': 'iā', 'ia2': 'iá',
        'ia3': 'iǎ', 'ia4': 'ià', 'ia5': 'ia', 'iao1': 'iāo', 'iao2': 'iáo',
        'iao3': 'iǎo', 'iao4': 'iào', 'iao5': 'iao', 'ie1': 'iē', 'ie2': 'ié',
        'ie3': 'iě', 'ie4': 'iè', 'ie5': 'ie', 'iu1': 'iū', 'iu2': 'iú',
        'iu3': 'iǔ', 'iu4': 'iù', 'iu5': 'iu', 'ian1': 'iān', 'ian2': 'ián',
        'ian3': 'iǎn', 'ian4': 'iàn', 'ian5': 'ian', 'in1': 'īn', 'in2': 'ín',
        'in3': 'ǐn', 'in4': 'ìn', 'in5': 'in', 'iang1': 'iāng',
        'iang2': 'iáng', 'iang3': 'iǎng', 'iang4': 'iàng', 'iang5': 'iang',
        'ing1': 'īng', 'ing2': 'íng', 'ing3': 'ǐng', 'ing4': 'ìng',
        'ing5': 'ing', 'ua1': 'uā', 'ua2': 'uá', 'ua3': 'uǎ', 'ua4': 'uà',
        'ua5': 'ua', 'uo1': 'uō', 'uo2': 'uó', 'uo3': 'uǒ', 'uo4': 'uò',
        'uo5': 'uo', 'uai1': 'uāi', 'uai2': 'uái', 'uai3': 'uǎi',
        'uai4': 'uài', 'uai5': 'uai', 'ui1': 'uī', 'ui2': 'uí', 'ui3': 'uǐ',
        'ui4': 'uì', 'ui5': 'ui', 'uan1': 'uān', 'uan2': 'uán', 'uan3': 'uǎn',
        'uan4': 'uàn', 'uan5': 'uan', 'un1': 'ūn', 'un2': 'ún', 'un3': 'ǔn',
        'un4': 'ùn', 'un5': 'un', 'uang1': 'uāng', 'uang2': 'uáng',
        'uang3': 'uǎng', 'uang4': 'uàng', 'uang5': 'uang', 'ue1': 'uē',
        'ue2': 'ué', 'ue3': 'uě', 'ue4': 'uè', 'ue5': 'ue', 've1': 'üē',
        've2': 'üé', 've3': 'üě', 've4': 'üè', 've5': 'üe', 'uan1': 'uān',
        'uan2': 'uán', 'uan3': 'uǎn', 'uan4': 'uàn', 'uan5': 'uan',
        'un1': 'ūn', 'un2': 'ún', 'un3': 'ǔn', 'un4': 'ùn', 'un5': 'un', }

    result = None
    for substring in string.split('_'):
        for src, target in replacements.items():
            p = re.compile('([b-df-hj-np-tv-z]+|^)' + src)
            if p.match(substring):
                if result:
                    result += ' ' + p.sub(r'\1' + target, substring)
                else:
                    result = p.sub(r'\1' + target, substring)
    return result
