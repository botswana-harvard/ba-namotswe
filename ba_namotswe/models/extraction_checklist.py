from django.db import models

from edc_constants.choices import YES_NO_UNKNOWN
from edc_constants.constants import UNKNOWN

from .crf_model import CrfModel


class ExtractionChecklist(CrfModel):

    arv_changes = models.CharField(
        max_length=20,
        verbose_name='Has the patient had an changes to his/her ARV regimen since previous visit?',
        choices=YES_NO_UNKNOWN,
        default=UNKNOWN)

    tb_diagnosis = models.CharField(
        max_length=20,
        verbose_name='Has the patient been diagnosed with TB since the last visit?',
        choices=YES_NO_UNKNOWN,
        default=UNKNOWN)

    oi_diagnosis = models.CharField(
        max_length=20,
        verbose_name='Has the patient been diagnosed with any new opportunistic infections since the last visit?',
        choices=YES_NO_UNKNOWN,
        default=UNKNOWN)

    assessment_history = models.CharField(
        max_length=20,
        verbose_name='Has there been any assessment history for the patient?',
        choices=YES_NO_UNKNOWN,
        default=UNKNOWN)

    extraction = models.CharField(
        max_length=20,
        verbose_name='Data extraction',
        choices=YES_NO_UNKNOWN,
        default=UNKNOWN)

    preg_diagnosis = models.CharField(
        max_length=20,
        verbose_name='Has this patient been diagnosed with a new pregnancy since the last visit?',
        choices=YES_NO_UNKNOWN,
        default=UNKNOWN)

    counselling_adhere = models.CharField(
        max_length=20,
        verbose_name='Was there any adherence counseling performed at this visit?',
        choices=YES_NO_UNKNOWN,
        default=UNKNOWN)

    transfer = models.CharField(
        max_length=20,
        verbose_name='Has this patient been transferred in or out of the clinic since the last visit?',
        choices=YES_NO_UNKNOWN,
        default=UNKNOWN)

    treatment = models.CharField(
        max_length=20,
        verbose_name='Does the patient have any treatment history?',
        choices=YES_NO_UNKNOWN,
        default=UNKNOWN)

    death = models.CharField(
        max_length=20,
        verbose_name='Has this patient died since the last visit?',
        choices=YES_NO_UNKNOWN,
        default=UNKNOWN)

    def __str__(self):
        return self.get_subject_identifier()

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
