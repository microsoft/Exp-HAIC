from django.core.management.base import BaseCommand, CommandError
import sys
import os
import csv
from pathlib import Path
from myapp.models import participant_info

class Command(BaseCommand):
    help = 'Populate db with participants data'
    
    def handle(self, *args, **options):
        path = Path(__file__)
        participant_path = os.path.join(path.parent.parent.parent.parent.absolute(), 'utils', 'data_for_experiment', 'participant_info.csv')
        with open(participant_path) as csv_file:
            reader = csv.DictReader(csv_file)
            print(reader)
            for line in reader:
                obj = participant_info()
                obj.participant_id = line['participant_id']
                obj.participant_numeric_id = line['participant_numeric_id']
                obj.state = line['state']
                obj.experience = line['experience']
                obj.exp_workflow = line['exp_workflow']
                obj.exp_group = line['exp_group']
                obj.save()
