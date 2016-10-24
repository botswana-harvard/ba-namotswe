from django.db import models

from .crf_model import CrfModel
from ..choices import PREGNANCY


class PregnancyHistory(CrfModel):

    pregnancy_details = models.CharField(
        max_length=7,
        verbose_name='Has the participant moved out of the household where last seen',
        choices=PREGNANCY,
        null=True,
        blank=False,
        help_text="")

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
