from django.db import models

from ..choices import YES_NO_UNCERTAIN

from .crf_model import CrfModel


class ExtractionChecklist(CrfModel):

    arv_changes = models.CharField(
        max_length=20,
        verbose_name='Has the patient had an changes to his/her ARV regimen since previous visit?',
        choices=YES_NO_UNCERTAIN)

    tb_diagnosis = models.CharField(
        max_length=20,
        verbose_name='Has the patient been diagnosed with TB since the last visit?',
        choices=YES_NO_UNCERTAIN)

    oi_diagnosis = models.CharField(
        max_length=20,
        verbose_name='Has the patient been diagnosed with any new opportunistic infections since the last visit?',
        choices=YES_NO_UNCERTAIN)

    assessment_history = models.CharField(
        max_length=20,
        verbose_name='Has there been any assessment history for the patient?',
        choices=YES_NO_UNCERTAIN)

    extraction = models.CharField(
        max_length=20,
        verbose_name='Data extraction',
        choices=YES_NO_UNCERTAIN)

    preg_diagnosis = models.CharField(
        max_length=20,
        verbose_name='Has this patient been diagnosed with a new pregnancy since the last visit?',
        choices=YES_NO_UNCERTAIN)

    counselling_adhere = models.CharField(
        max_length=20,
        verbose_name='Was there any adherence counseling performed at this visit?',
        choices=YES_NO_UNCERTAIN)

    transfer = models.CharField(
        max_length=20,
        verbose_name='Has this patient been transferred in or out of the clinic since the last visit?',
        choices=YES_NO_UNCERTAIN)

    treatment = models.CharField(
        max_length=20,
        verbose_name='Does the patient have any treatment history?',
        choices=YES_NO_UNCERTAIN)

    death = models.CharField(
        max_length=20,
        verbose_name='Has this patient died since the last visit?',
        choices=YES_NO_UNCERTAIN)

    def __str__(self):
        return self.get_subject_identifier()

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
