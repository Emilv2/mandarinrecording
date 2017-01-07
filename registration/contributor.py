from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contributor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    MALE = 'M'
    FEMALE = 'F'
    NO_ANSWER = 'N'
    SEX_CHOISES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
        (NO_ANSWER, _('No answer')))
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOISES)

    accepted_license = models.BooleanField(
        blank=False,
        default=False
    )

    syllables_list = models.CharField(
        max_length=700,
        default='')

    @classmethod
    def create(cls, user, sex):
        contributor = cls(user=user, sex=sex)
        return contributor

    def get_base_syllables_list(this):
        if len(this.syllables_list) == 0:
            return []
        else:
            return this.syllables_list[0:-1].split(';')

    def set_base_syllables_list(this, lst):
        tmp = ''
        for i in lst:
            tmp += i + ';'
        this.syllables_list = tmp
        this.save()

    def pop_base_syllables_list(this, string):
        lst = this.get_base_syllables_list()
        try:
            index = lst.index(string)
            lst.pop(index)
            this.set_base_syllables_list(lst)
        except ValueError:
            pass
