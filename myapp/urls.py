from django.urls import path

from . import views

urlpatterns = [
    path("diagnosistask/", views.home, name="home"),
    path(
        "diagnosistask/participant_id",
        views.request_participantid,
        name="request_participantid",
    ),
    path("diagnosistask/<participant_id>", views.show_exp_stage, name="show_exp_stage"),
    path(
        "diagnosistask/<participant_id>/<int:exp_stage>/instructions_main",
        views.instructions_main,
        name="instructions_main",
    ),
    path(
        "diagnosistask/<participant_id>/<int:exp_stage>/instructions_aiinfo",
        views.instructions_aiinfo,
        name="instructions_aiinfo",
    ),
    path(
        "diagnosistask/<participant_id>/<int:exp_stage>/instructions_aiadditionalhelp",
        views.instructions_aiadditionalhelp,
        name="instructions_aiadditionalhelp",
    ),
    path(
        "diagnosistask/<participant_id>/<int:exp_stage>/instructions_choiceaihelp",
        views.instructions_choiceaihelp,
        name="instructions_choiceaihelp",
    ),
    path(
        "diagnosistask/<participant_id>/<int:exp_stage>/start_experiment",
        views.instructions_startexperiment,
        name="instructions_startexperiment",
    ),
    path(
        "diagnosistask/<participant_id>/<int:exp_stage>/<int:image_order>-<int:exp_aipresence>",
        views.diagnosistask,
        name="diagnosistask",
    ),
    path(
        "diagnosistask/<participant_id>/<int:exp_stage>/comprehension_questions",
        views.comprehension_questions,
        name="comprehension_questions",
    ),
    path(
        "diagnosistask/<participant_id>/<int:exp_stage>/instructions_ondemand",
        views.instructions_ondemand,
        name="instructions_ondemand",
    ),
    path(
        "diagnosistask/<participant_id>/<int:exp_stage>/questionnaire",
        views.stage_questionnaire,
        name="stage_questionnaire",
    ),
    path(
        "diagnosistask/<participant_id>/<int:exp_stage>/end_stage",
        views.end_stage,
        name="end_stage",
    ),
]
