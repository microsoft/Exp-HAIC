import pandas as pd
from myapp.models import *


df = pd.DataFrame(list(diagnosis.objects.all().values()))
df.to_csv("./utils/data_db2csv/diagnosis.csv")

df = pd.DataFrame(list(survey_responses.objects.all().values()))
df.to_csv("./utils/data_db2csv/survey_responses.csv")

df = pd.DataFrame(list(survey_aiuseful.objects.all().values()))
df.to_csv("./utils/data_db2csv/survey_aiuseful.csv")

df = pd.DataFrame(list(participant_info.objects.all().values()))
df.to_csv("./utils/data_db2csv/participant_info.csv")

df = pd.DataFrame(list(participant_exp.objects.all().values()))
df.to_csv("./utils/data_db2csv/participant_exp.csv")

df = pd.DataFrame(list(participant_stage_completed.objects.all().values()))
df.to_csv("./utils/data_db2csv/participant_stage_completed.csv")

df = pd.DataFrame(list(aipreds.objects.all().values()))
df.to_csv("./utils/data_db2csv/aipreds.csv")

df = pd.DataFrame(list(timepage.objects.all().values()))
df.to_csv("./utils/data_db2csv/timepage.csv")

df = pd.DataFrame(list(aiinfo_default.objects.all().values()))
df.to_csv("./utils/data_db2csv/aiinfo_default.csv")

df = pd.DataFrame(list(timepage.objects.all().values()))
df.to_csv("./utils/data_db2csv/timepage.csv")
