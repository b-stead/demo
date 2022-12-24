from django.db import models
from django_resized import ResizedImageField
from datetime import datetime
from django.utils import timezone

# Create your models here.

GENDER = (
    (None, 'Choose your gender'),
    ('0', 'male'),
    ('1', 'female'),
    ('3', 'other'),
)

DISCIPLINE = (
    (None, 'Choose your primary discipline'),
    ('0', 'kayak'),
    ('1', 'canoe'),
    ('2', 'sup'),
)

CLASSIFICATION = (
    ('0', 'able-bodied'),
    ('1', 'para-canoe'),
)


class Coach(models.Model):
    name = models.CharField(max_length=40, blank=True)
    bio = models.CharField(max_length=400, null=True, blank=True)
    profile_pic = ResizedImageField(size=[50, 80], quality=100, default=None, null=True, blank=True)
    location = models.TextField(blank=True)
    

    def __str__(self):
        return self.name

class Athlete(models.Model):
    name = models.CharField(max_length=40, blank=True)
    bio = models.CharField(max_length=400, null=True, blank=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, null=True)
    DOB = models.DateField(verbose_name='Date of Birth')
    gender = models.CharField(max_length=6, choices=GENDER, verbose_name="gender")
    discipline = models.CharField(max_length=6, choices=DISCIPLINE, verbose_name="discipline", blank=True)
    classification = models.CharField(max_length=12, choices=CLASSIFICATION, verbose_name="classification", blank=True)
    club = models.CharField(max_length=50, verbose_name="club", blank=True)
    profile_pic = ResizedImageField(size=[50, 80], quality=100, upload_to="athlete", default=None, null=True, blank=True)

    @property
    def age(self):
        return int((datetime.now().date() - self.DOB).days / 365.25)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=40, blank=True)
    coaches = models.ManyToManyField(Coach)
    athletes = models.ManyToManyField(Athlete)
    profile_pic = ResizedImageField(size=[50, 80], quality=100, upload_to="team", default=None, null=True, blank=True)

    def __str__(self):
        return self.name


