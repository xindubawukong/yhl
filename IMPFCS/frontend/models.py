from django.db import models
from django.contrib.auth.models import User


class BasicInfo(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    MALE = 'male'
    FEMALE = 'female'
    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female')
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    @staticmethod
    def fields():
        return set(BasicInfo._meta.get_all_field_names()).difference({'user', 'user_id', 'id'})

class AthleteInfo(models.Model):
    user = models.OneToOneField(User)
    GPA = models.DecimalField(max_digits=5, decimal_places=2)