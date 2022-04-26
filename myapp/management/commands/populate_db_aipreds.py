from django.core.management.base import BaseCommand, CommandError
import sys
import os
import csv
from pathlib import Path
from myapp.models import aipreds

class Command(BaseCommand):
    help = 'Populate db with ai predictions'
    
    def handle(self, *args, **options):
        path = Path(__file__)
        file_path = os.path.join(path.parent.parent.parent.parent.absolute(), 'utils', 'data_for_experiment', 'aipreds_with_eof.csv')
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for line in reader:
                obj = aipreds()
                obj.image_id = line['image_id']
                obj.condition = line['condition']
                obj.grouping = line['grouping']
                obj.condition_short = line['condition_short']
                obj.pred = line['pred']
                obj.round_pred = round(float(line['round_pred']))
                obj.accuracy_x_condition_x_binpred = float(line['acc'])
                obj.round_accuracy_x_condition_x_binpred = line['acc_floor1to99']
                obj.y = line['y']
                obj.save()
