from django.db import models
from django.core.management.base import BaseCommand
BaseCommand.requires_system_checks = False

class participant_info(models.Model):

    participant_id = models.CharField(max_length=200, default="")
    participant_numeric_id = models.IntegerField(default="-1")
    state = models.CharField(max_length=200, default="")
    experience = models.IntegerField(
        help_text="Experience: 1 with experience, 0 otherwise", default=-1
    )
    exp_workflow = models.IntegerField(
        help_text="Workflow: 1 one-step prediction, 0 two-step prediction", default=-1
    )
    exp_group = models.IntegerField(help_text="Group assignment", default=-1)

    def __str__(self):
        return self.participant_id


class participant_exp(models.Model):

    participant_id = models.CharField(max_length=200, default="")
    participant_numeric_id = models.IntegerField(default="-1")
    email = models.EmailField(max_length=1000, default="")
    experience = models.IntegerField(
        help_text="Experience: 1 with experience, 0 otherwise", default=-1
    )
    exp_stage = models.IntegerField(help_text="Day of experiment", default=-1)
    exp_workflow = models.IntegerField(
        help_text="Workflow: 1 one-step prediction, 0 two-step prediction", default=-1
    )
    exp_group = models.IntegerField(help_text="Group assignment", default=-1)
    image_id = models.CharField(max_length=1000, default=-1)
    image_order = models.IntegerField(default=-1)
    exp_aism = models.IntegerField(default=-1)
    exp_aieof = models.IntegerField(default=-1)


class participant_stage_completed(models.Model):

    participant_id = models.CharField(max_length=200, default="")
    exp_stage = models.IntegerField(help_text="Day of experiment", default=-1)


class aiinfo_default(models.Model):  # model for stage 10

    participant_id = models.CharField(max_length=200, default="")
    default_airec = models.IntegerField(default=-1)
    default_aiconf = models.IntegerField(default=-1)
    default_aieof = models.IntegerField(default=-1)


class survey_aiuseful(models.Model):  # model for question on AI for each case

    participant_id = models.CharField(max_length=200, default="")
    exp_stage = models.IntegerField(default=-1)
    image_order = models.IntegerField(default=-1)
    aiuseful = models.CharField(max_length=3, default="", null=True)


class survey_responses(models.Model):

    participant_id = models.CharField(max_length=200, default="")
    exp_stage = models.IntegerField(default="-1")
    workload_demanding = models.TextField(default="")
    workload_frustrating = models.TextField(default="")
    confidence_increase = models.TextField(default="")
    usefulness_quickly = models.TextField(default="")
    usefulness_accuracy = models.TextField(default="")
    confidence_aifocus = models.TextField(default="", null=True)
    usefulness_eof = models.TextField(default="", null=True)
    usefulness_whenmosthelpful = models.TextField(default="")
    usefulness_whenleasthelpful = models.TextField(default="")
    trust_whenpresent = models.TextField(default="")
    trust_whennotpresent = models.TextField(default="")
    trust_howfinalrec = models.TextField(default="")
    trust_understandmistakes = models.TextField(default="")
    trust_errorsmade = models.TextField(default="")
    trust_whentrustai = models.TextField(default="")
    futureuse_daily = models.TextField(default="")
    elaborate = models.TextField(default="")
    rank_usefulness_confidence = models.TextField(default="", null=True)
    rank_usefulness_aifocus = models.TextField(default="", null=True)
    rank_usefulness_eof = models.TextField(default="", null=True)


class timepage(models.Model):
    participant_id = models.CharField(max_length=200, default="")
    exp_stage = models.IntegerField(default="-1")
    page = models.CharField(max_length=1000, default="")
    time = models.DateTimeField(auto_now_add=True)


class aipreds(models.Model):
    image_id = models.CharField(max_length=1000, default="")
    condition = models.CharField(max_length=1000, default="")
    pred = models.DecimalField(max_digits=5, decimal_places=3)
    bin_pred = models.IntegerField(default=-1)
    round_pred = models.IntegerField(default=-1)
    y = models.IntegerField(default=-1)
    condition_short = models.CharField(max_length=1000, default="")
    grouping = models.CharField(max_length=1000, default="")
    accuracy_x_condition_x_binpred = models.IntegerField(default=-1)
    round_accuracy_x_condition_x_binpred = models.IntegerField(default=-1)


class diagnosis(models.Model):

    participant_id = models.CharField(max_length=200, default="")
    exp_stage = models.IntegerField(default=-1)
    exp_aipresence = models.IntegerField(default=-1)
    image_order = models.IntegerField(default=-1)
    diag_condname = models.CharField(max_length=10, default="")
    diag_condpresent = models.CharField(max_length=10, default="")
    diag_lklpresent = models.IntegerField(default=-1)
    diag_secop = models.CharField(max_length=10, default="")
    diag_aifocustime = models.CharField(max_length=10, default="", null=True)
    diag_qaifocus = models.CharField(max_length=10, default="", null=True)
    diag_aiconftime = models.CharField(max_length=10, default="", null=True)
    diag_aieoftime = models.CharField(max_length=10, default="", null=True)
    diag_airectime = models.CharField(max_length=10, null=True)
    time_completed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.participant_id
