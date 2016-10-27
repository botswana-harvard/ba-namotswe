from django.db import models
from django.utils import timezone

from edc_constants.constants import UNKNOWN

from ..choices import WHO_STAGE, WHO_DEFINING_ILLNESSES

from .crf_model import CrfModel


class WhoStaging(CrfModel):

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    who_stage = models.CharField(
        max_length=25,
        choices=WHO_STAGE,
        default=UNKNOWN)

    comment = models.TextField(
        max_length=250,
        null=True,
        blank=True)

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'WHO Staging'
        verbose_name_plural = 'WHO Staging'


class WhoDiagnosis(models.Model):

    who_staging = models.ForeignKey(WhoStaging)

    dx = models.CharField(
        max_length=200,
        choices=WHO_DEFINING_ILLNESSES)

    dx_date = models.DateField(
        null=True,
        blank=True,
        help_text='Provide if known')

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
