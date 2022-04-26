from django.shortcuts import render
from django.http import (
    HttpResponseRedirect,
    HttpResponseNotFound,
    Http404,
)
from django.utils import timezone
from .models import (
    diagnosis,
    survey_responses,
    survey_aiuseful,
    participant_info,
    participant_exp,
    aipreds,
    timepage,
    aiinfo_default,
    participant_stage_completed,
)

# load global variables here
all_participant_id = list(
    participant_info.objects.values_list("participant_id", flat=True)
)
all_participant_numeric_id = list(
    participant_info.objects.values_list("participant_numeric_id", flat=True)
)


def check_pars_url(participant_id=1, exp_stage=1, image_order=1, exp_aipresence=1):
    if (
        participant_id not in all_participant_id
        or image_order not in [x for x in range(1, 21)]
        or exp_stage not in [x for x in range(1, 11)]
        or exp_aipresence not in [0, 1]
    ):
        raise Http404(
            "Please check your participant ID, experimental stage, and case number"
        )


# initial webpage
def home(request):

    if request.method == "POST":
        return HttpResponseRedirect("participant_id")

    return render(request, "myapp/instructions_home.html")


# get participant id
def request_participantid(request):

    if request.method == "POST":
        participant_numeric_id = str.strip(request.POST.get("participant_id"))
        if participant_numeric_id in [str(x) for x in all_participant_numeric_id]:
            participant_id = participant_info.objects.filter(
                participant_numeric_id=participant_numeric_id
            ).values_list("participant_id", flat=True)
            return HttpResponseRedirect(participant_id[0])
        else:
            return render(
                request,
                "myapp/initial_enterstudy_requestparticipantid.html",
                {
                    "participant_ids": all_participant_numeric_id,
                    "show_info": 1,
                    "message": 1,
                },
            )

    return render(
        request,
        "myapp/initial_enterstudy_requestparticipantid.html",
        {
            "participant_ids": all_participant_numeric_id,
            "show_info": 0,
            "message": 0,
        },
    )


# show stage to be completed
def show_exp_stage(request, participant_id):

    # completed stages
    stages_done = participant_stage_completed.objects.filter(
        participant_id=participant_id
    ).values_list("exp_stage", flat=True)
    if stages_done:
        exp_stage = max(stages_done) + 1
    else:
        exp_stage = 1

    participant_numeric_id = participant_info.objects.filter(
        participant_id=participant_id
    ).values_list("participant_numeric_id", flat=True)[0]
    if request.method == "POST":
        return HttpResponseRedirect(
            str(participant_id) + "/" + str(exp_stage) + "/instructions_main"
        )

    return render(
        request,
        "myapp/initial_show_status_experiment.html",
        {"participant_numeric_id": participant_numeric_id, "exp_stage": exp_stage},
    )


def instructions_ondemand(request, participant_id, exp_stage):
    if request.method == "GET":
        timepage(
            participant_id=participant_id,
            exp_stage=exp_stage,
            page="instructions_ondemand",
            time=timezone.now(),
        ).save()
    if request.method == "POST":
        if request.POST.get("next"):
            return HttpResponseRedirect("comprehension_questions")
        else:
            return HttpResponseRedirect("instructions_aiinfo")
    return render(request, "myapp/instructions_on_demand.html")


def instructions_main(request, participant_id, exp_stage):
    if request.method == "GET":
        timepage(
            participant_id=participant_id,
            exp_stage=exp_stage,
            page="instructions_main",
            time=timezone.now(),
        ).save()
    if request.method == "POST":
        return HttpResponseRedirect("instructions_aiinfo")
    return render(request, "myapp/instructions_main.html")


def instructions_aiinfo(request, participant_id, exp_stage):
    workflow = participant_info.objects.filter(
        participant_id=participant_id
    ).values_list("exp_workflow", flat=True)[0]
    if request.method == "GET":
        timepage(
            participant_id=participant_id,
            exp_stage=exp_stage,
            page="instructions_aiinfo",
            time=timezone.now(),
        ).save()
    if request.method == "POST":
        participant_info_stage = participant_exp.objects.filter(
            participant_id=participant_id, exp_stage=exp_stage
        )
        exp_aism = participant_info_stage.values_list("exp_aism", flat=True)[0]
        exp_aieof = participant_info_stage.values_list("exp_aieof", flat=True)[0]
        if (
            exp_stage >= 3
            and exp_stage <= 8
            and (exp_aieof == 1 or exp_aism == 1)
            and request.POST.get("next")
        ):
            return HttpResponseRedirect("instructions_aiadditionalhelp")
        elif exp_stage == 9 and request.POST.get("next"):
            return HttpResponseRedirect("instructions_ondemand")
        elif exp_stage == 10 and request.POST.get("next"):
            return HttpResponseRedirect("instructions_choiceaihelp")
        elif request.POST.get("next"):
            return HttpResponseRedirect("comprehension_questions")
        else:
            return HttpResponseRedirect("instructions_main")
    return render(request, "myapp/instructions_aiinfo.html", {"workflow": workflow})


def instructions_choiceaihelp(request, participant_id, exp_stage):
    if request.method == "GET":
        timepage(
            participant_id=participant_id,
            exp_stage=exp_stage,
            page="choice_aihelp",
            time=timezone.now(),
        ).save()

    if aiinfo_default.objects.filter(participant_id=participant_id).values_list(
        "participant_id", flat=True
    ):
        default_already_chosen = True
    else:
        default_already_chosen = False

    if request.method == "POST":
        if request.POST.get("next"):
            if not default_already_chosen:
                aiinfo_default(
                    participant_id=participant_id,
                    default_airec=1 if request.POST.get("airec") == "yes" else 0,
                    default_aiconf=1 if request.POST.get("aiconf") == "yes" else 0,
                    default_aieof=1 if request.POST.get("aieof") == "yes" else 0,
                ).save()
            return HttpResponseRedirect("comprehension_questions")
        else:
            return HttpResponseRedirect("instructions_aiinfo")
    return render(
        request,
        "myapp/instructions_choiceaihelp.html",
        {"default_already_chosen": default_already_chosen},
    )


def instructions_aiadditionalhelp(request, participant_id, exp_stage):
    if request.method == "GET":
        timepage(
            participant_id=participant_id,
            exp_stage=exp_stage,
            page="instructions_aiadditionalhelp",
            time=timezone.now(),
        ).save()
    participant_info_stage = participant_exp.objects.filter(
        participant_id=participant_id, exp_stage=exp_stage
    )
    exp_aism = participant_info_stage.values_list("exp_aism", flat=True)[0]
    exp_aieof = participant_info_stage.values_list("exp_aieof", flat=True)[0]
    if request.method == "POST":
        if request.POST.get("next"):
            return HttpResponseRedirect("comprehension_questions")
        else:
            return HttpResponseRedirect("instructions_aiinfo")
    return render(
        request,
        "myapp/instructions_aiadditionalinfo.html",
        {"exp_aism": exp_aism, "exp_aieof": exp_aieof, "exp_stage": exp_stage},
    )


def comprehension_questions(request, participant_id, exp_stage):
    if request.method == "GET":
        timepage(
            participant_id=participant_id,
            exp_stage=exp_stage,
            page="comprehension_question",
            time=timezone.now(),
        ).save()
    if request.method == "POST":
        return HttpResponseRedirect("start_experiment")
    return render(request, "myapp/comprehension_questions.html")


def instructions_startexperiment(request, participant_id, exp_stage):
    if request.method == "GET":
        timepage(
            participant_id=participant_id,
            exp_stage=exp_stage,
            page="instructions_startexperiment",
            time=timezone.now(),
        ).save()
    if request.method == "POST":
        workflow = participant_info.objects.filter(
            participant_id=participant_id
        ).values_list("exp_workflow", flat=True)[0]
        if workflow == 0:
            return HttpResponseRedirect("1-0")
        else:
            return HttpResponseRedirect("1-1")
    return render(request, "myapp/instructions_startexperiment.html")


def diagnosistask(request, participant_id, exp_stage, image_order, exp_aipresence):

    # temporary message
    # if exp_stage > 2:
    #     raise Http404(
    #         "We need to analyze the data before you can start stage 3. Thank you!"
    #     )

    all_condition_short = list(
        aipreds.objects.values_list("condition_short", flat=True).distinct()
    )
    all_condition_short = filter(lambda x: x != "", all_condition_short)

    if request.method == "GET":
        check_pars_url(
            participant_id=participant_id,
            exp_stage=exp_stage,
            image_order=image_order,
            exp_aipresence=exp_aipresence,
        )

    # get workflow
    exp_workflow = participant_info.objects.filter(
        participant_id=participant_id
    ).values_list("exp_workflow", flat=True)[0]

    # redirect to task with AI in case of 1-step workflow
    if exp_workflow == 1 and exp_aipresence == 0:
        return HttpResponseRedirect(str(image_order) + "-1")

    # check that participants are in the correct stage
    stages_done = participant_stage_completed.objects.filter(
        participant_id=participant_id
    ).values_list("exp_stage", flat=True)
    if stages_done:
        exp_stage_todo = max(stages_done) + 1
    else:
        exp_stage_todo = 1
    if exp_stage != exp_stage_todo:
        raise Http404("You are in the wrong stage! Please fix your URL")

    if exp_stage == 10:
        default_aiinfo = aiinfo_default.objects.filter(
            participant_id=participant_id
        ).values_list("default_airec", "default_aiconf", "default_aieof")
        defaults = {
            "airec": [x[0] for x in default_aiinfo][0],
            "aiconf": [x[1] for x in default_aiinfo][0],
            "aieof": [x[2] for x in default_aiinfo][0],
        }
    else:
        defaults = {"airec": 0, "aiconf": 0, "aieof": 0}

    if request.method == "GET":

        # find image id
        participant_exp_x_image = participant_exp.objects.filter(
            participant_id=participant_id, exp_stage=exp_stage, image_order=image_order
        )
        image_id = participant_exp_x_image.values_list("image_id", flat=True)[0]
        image_preds = list(aipreds.objects.filter(image_id=image_id).values()) 

        # load user parameters parameters
        exp_aism = participant_exp_x_image.values_list("exp_aism", flat=True)[0]
        exp_aieof = participant_exp_x_image.values_list("exp_aieof", flat=True)[0]

        # load tasks that have already been completed
        tasks_done = (
            diagnosis.objects.filter(participant_id=participant_id, exp_stage=exp_stage)
            .values("image_order", "exp_aipresence")
            .distinct()
            .values_list("image_order", "exp_aipresence")
        )
        images_done = [x[0] for x in tasks_done]
        aipresence_done = [x[1] for x in tasks_done]
        # send participants to case that they are supposed to complete, if
        # they are not already on the correct case. First look if one of previous
        # cases has not been evaluated yet
        for img in range(1, image_order + 1):
            # if participant has not completed one of the previous cases without the AI help
            # or the image without AI help has not been evaluated yet
            if exp_workflow == 0 and (img, 0) not in tasks_done and exp_aipresence != 0:
                return HttpResponseRedirect(str(img) + "-0")
            # if image with the AI help has not been evaluated before
            elif (img, 1) not in tasks_done and img != image_order:
                return HttpResponseRedirect(str(img) + "-1")
        # if case has already been evaluated, then redirect to the next case that needs to be done
        if (img, exp_aipresence) in tasks_done:
            for img in range(1, 21):
                if exp_workflow == 0 and (img, 0) not in tasks_done:
                    return HttpResponseRedirect(str(img) + "-0")
                if (img, 1) not in tasks_done:
                    return HttpResponseRedirect(str(img) + "-1")

        # if user has already made a choice, reload choice
        # used for second step of 2-step workflow
        past_choices = diagnosis.objects.filter(
            participant_id=participant_id,
            exp_stage=exp_stage,
            image_order=image_order,
            exp_aipresence=1,
        )
        if exp_aipresence == 0 or len(past_choices) == 0:
            past_choices = diagnosis.objects.filter(
                participant_id=participant_id,
                exp_stage=exp_stage,
                image_order=image_order,
                exp_aipresence=0,
            )
        if past_choices:
            for condnum in range(0, len(image_preds)):
                image_preds[condnum]["diag_condpresent"] = (
                    "checked"
                    if past_choices.filter(
                        diag_condname=image_preds[condnum]["condition_short"]
                    )
                    .order_by("-time_completed")
                    .values_list("diag_condpresent", flat=True)[0]
                    == "yes"
                    else "placeholder"
                )
                image_preds[condnum]["diag_lklpresent"] = str(
                    past_choices.filter(
                        diag_condname=image_preds[condnum]["condition_short"]
                    )
                    .order_by("-time_completed")
                    .values_list("diag_lklpresent", flat=True)[0]
                )
                image_preds[condnum]["diag_secop"] = (
                    "checked"
                    if past_choices.filter(
                        diag_condname=image_preds[condnum]["condition_short"]
                    )
                    .order_by("-time_completed")
                    .values_list("diag_secop", flat=True)[0]
                    == "yes"
                    else "placeholder"
                )

        # store time page is accessed
        timepage(
            participant_id=participant_id,
            exp_stage=exp_stage,
            page="diagnosistask-" + str(image_order) + "-" + str(exp_aipresence),
            time=timezone.now(),
        ).save()


    if request.method == "POST":

        for condition in all_condition_short:

            obj = diagnosis()
            obj.participant_id = participant_id
            obj.exp_stage = exp_stage
            obj.exp_aipresence = exp_aipresence
            obj.image_order = image_order

            obj.diag_condname = condition
            obj.diag_condpresent = request.POST.get("condpresent-" + condition)
            obj.diag_lklpresent = request.POST.get("sliderprob-" + condition)
            obj.diag_secop = request.POST.get("secondopinion-" + condition)
            obj.diag_qaifocus = request.POST.get("qaifocus-" + condition)

            # timestamp for AI focus show (could be null)
            obj.diag_aifocustime = request.POST.get(
                "aifocus-" + condition + "-timestamp"
            )
            obj.diag_aieoftime = request.POST.get("aieof-" + condition + "-timestamp")
            obj.diag_aiconftime = request.POST.get("aiconf-" + condition + "-timestamp")
            obj.diag_airectime = request.POST.get("airec-timestamp")
            obj.time_completed = timezone.now()

            obj.save()

        if exp_aipresence == 1:
            obj = survey_aiuseful()
            obj.participant_id = participant_id
            obj.exp_stage = exp_stage
            obj.image_order = image_order
            obj.aiuseful = request.POST.get("qtool-help")
            obj.save()

        if (
            exp_aipresence == 1 and image_order == 20
        ):  # AI has been shown and we reached the end of survey
            if exp_stage % 2 == 0:
                return HttpResponseRedirect("questionnaire")
            else:
                return HttpResponseRedirect("end_stage")
        elif (
            exp_aipresence == 1 and exp_workflow == 0
        ):  # AI has been shown and two-step workflow
            return HttpResponseRedirect(str(image_order + 1) + "-0#cond-Cardiomegaly")
        elif (
            exp_aipresence == 0 and exp_workflow == 0
        ):  # AI has not been shown yet and two-step workflow
            return HttpResponseRedirect(str(image_order) + "-1#cond-Cardiomegaly")
        else:  # proceed to next image
            return HttpResponseRedirect(str(image_order + 1) + "-1#cond-Cardiomegaly")


    if request.method == "GET":
        return render(
            request,
            "myapp/diagnosistask.html",
            {
                "image_order": image_order,
                "image_id": 'img',#image_id, # when using real images with different ids, uncomment image_id
                "participant_id": participant_id,
                "image_preds": image_preds,
                "exp_stage": exp_stage,
                "exp_aipresence": exp_aipresence,
                "exp_aism": exp_aism,
                "exp_aieof": exp_aieof,
                "default_airec": defaults["airec"],
                "default_aieof": defaults["aieof"],
                "default_aiconf": defaults["aiconf"],
                "possible_groupings": [
                    "Cardiovascular",
                    "Extra Thoracic",
                    "Mediastinal Structures",
                    "Pleural Space",
                    "Pulmonary Structures",
                ],
            },
        )



def stage_questionnaire(request, participant_id, exp_stage):

    if request.method == "GET":
        timepage(
            participant_id=participant_id,
            exp_stage=exp_stage,
            page="stage_questionnaire",
            time=timezone.now(),
        ).save()

    participant_info_stage = participant_exp.objects.filter(
        participant_id=participant_id, exp_stage=exp_stage
    )
    exp_aism = participant_info_stage.values_list("exp_aism", flat=True)[0]
    exp_aieof = participant_info_stage.values_list("exp_aieof", flat=True)[0]

    if exp_stage % 2 != 0:
        return HttpResponseNotFound("Page not found")

    if request.method == "POST":

        obj = survey_responses()
        obj.participant_id = participant_id
        obj.exp_stage = exp_stage
        obj.workload_demanding = request.POST.get("workload-demanding")
        obj.workload_frustrating = request.POST.get("workload-frustrating")
        obj.confidence_increase = request.POST.get("confidence-increase")
        obj.usefulness_quickly = request.POST.get("usefulness-quickly")
        obj.usefulness_accuracy = request.POST.get("usefulness-accuracy")
        obj.confidence_aifocus = request.POST.get("usefulness-aifocus")
        obj.usefulness_eof = request.POST.get("usefulness-eof")
        obj.usefulness_whenmosthelpful = request.POST.get("usefulness-whenmosthelpful")
        obj.usefulness_whenleasthelpful = request.POST.get(
            "usefulness-whenleasthelpful"
        )
        obj.trust_whenpresent = request.POST.get("trust-whenpresent")
        obj.trust_whennotpresent = request.POST.get("trust-whennotpresent")
        obj.trust_howfinalrec = request.POST.get("trust-howfinalrec")
        obj.trust_understandmistakes = request.POST.get("trust-understandmistakes")
        obj.trust_errorsmade = request.POST.get("trust-errorsmade")
        obj.trust_whentrustai = request.POST.get("trust-whentrustai")
        obj.futureuse_daily = request.POST.get("futureuse-daily")
        obj.elaborate = request.POST.get("elaborate")
        obj.rank_usefulness_confidence = request.POST.get("rank-usefulness-confidence")
        obj.rank_usefulness_aifocus = request.POST.get("rank-usefulness-aifocus")
        obj.rank_usefulness_eof = request.POST.get("rank-usefulness-eof")

        obj.save()

        return HttpResponseRedirect("end_stage")

    return render(
        request,
        "myapp/stage_questionnaire.html",
        {
            "participant_id": participant_id,
            "exp_stage": exp_stage,
            "exp_aism": exp_aism,
            "exp_aieof": exp_aieof,
        },
    )


def end_stage(request, participant_id, exp_stage):

    # check participants have answered all questions
    tasks_done = diagnosis.objects.filter(
        participant_id=participant_id, exp_stage=exp_stage, exp_aipresence=1
    ).values_list("image_order", flat=True)
    if tasks_done:
        if max(tasks_done) == 20:
            # do not check if survey has been done
            # save stage as being completed
            obj = participant_stage_completed()
            obj.participant_id = participant_id
            obj.exp_stage = exp_stage
            obj.save()

    if request.method == "GET":
        timepage(
            participant_id=participant_id,
            exp_stage=exp_stage,
            page="end_stage",
            time=timezone.now(),
        ).save()

    return render(
        request,
        "myapp/end_stage.html",
        {"participant_id": participant_id, "exp_stage": exp_stage},
    )
