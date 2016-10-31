from django.db import models
from django.utils import timezone

from edc_constants.constants import UNKNOWN

from ..choices import WHO_STAGE, WHO_DEFINING_ILLNESSES

from .crf_model_mixin import CrfModelMixin, CrfInlineModelMixin


class WhoStaging(CrfModelMixin):

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    who_stage = models.CharField(
        verbose_name='WHO stage',
        max_length=25,
        choices=WHO_STAGE,
        default=UNKNOWN)

    class Meta(CrfModelMixin.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'WHO Staging'
        verbose_name_plural = 'WHO Staging'


class WhoDiagnosis(CrfInlineModelMixin):

    who_staging = models.ForeignKey(WhoStaging)

    dx = models.CharField(
        max_length=200,
        choices=WHO_DEFINING_ILLNESSES)

    dx_date = models.DateField(
        null=True,
        blank=True,
        help_text='Provide if known')

    class Meta(CrfInlineModelMixin.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'WHO Diagnosis'
        verbose_name_plural = 'WHO Diagnosis'
        unique_together = (('who_staging', 'dx', 'dx_date'), )
        crf_inline_parent = 'who_staging'
