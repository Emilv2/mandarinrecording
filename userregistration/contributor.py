from django.contrib.auth.models import User
from django.db import models

class Contributor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    MALE = 'M'
    FEMALE = 'F'
    NO_ANSWER = 'N'
    SEX_CHOISES = (
            (MALE, 'Male'),
            (FEMALE, 'Female'),
            (NO_ANSWER, 'No answer'))
    sex = models.CharField(
            max_length=1,
            choices=SEX_CHOISES)

    @classmethod
    def create(cls, user, sex):
        contributor = cls(user=user, sex=sex)
        return contributor
