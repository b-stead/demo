import csv
from datetime import date
from itertools import islice
from django.conf import settings
from django.core.management.base import BaseCommand
from team.models import Athlete

#run manage.py load_users

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'team' / 'data' / 'users.csv'

        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(islice(csvfile, None))

            for row in reader:
                Athlete.objects.get_or_create(
                    gender=row['gender'],
                    name=row['name'],
                    bio=row['bio'],
                    coach_id=row['coach_id'],
                    DOB=row['DOB'],
                    discipline=row['discipline'],
                    classification=row['classification'],
                    club=row['club'],
                    
                    )