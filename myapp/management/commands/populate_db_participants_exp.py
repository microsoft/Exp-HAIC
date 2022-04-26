from django.core.management.base import BaseCommand, CommandError
import sys
import os
import csv
from pathlib import Path
from myapp.models import participant_exp

class Command(BaseCommand):
    help = 'Populate db with participants experiment data'
    
    def handle(self, *args, **options):
        path = Path(__file__)
        participant_path = os.path.join(path.parent.parent.parent.parent.absolute(), 'utils', 'data_for_experiment', 'conditions.csv')
        with open(participant_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for line in reader:
                obj = participant_exp()
                obj.participant_id = line['participant_id']
                obj.participant_numeric_id = line['participant_numeric_id']
                obj.experience = line['experience']
                obj.exp_workflow = line['exp_workflow']
                obj.exp_group = line['exp_group']
                obj.exp_stage = line['exp_stage']
                obj.image_id = line['image_id']
                obj.image_order = line['image_order']
                obj.exp_aism = line['exp_aism']
                obj.exp_aieof = line['exp_aieof']
                obj.save()
