import csv
from datetime import date
from itertools import islice
from django.conf import settings
from django.core.management.base import BaseCommand
from team.models import Coach

#run manage.py load_users

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'team' / 'data' / 'coach_users.csv'

        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(islice(csvfile, None))

            for row in reader:
                Coach.objects.get_or_create(
                    name=row['name'],
                    location=row['location'],
                    bio=row['bio'],
                    )