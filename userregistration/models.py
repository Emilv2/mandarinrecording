from django.db import models
from enum import Enum

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
