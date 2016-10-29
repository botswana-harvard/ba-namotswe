from django.db import models

from .crf_model import CrfModelMixin
from ..choices import RELATIONSHIP
from edc_constants.constants import UNKNOWN


class AdherenceCounselling(CrfModelMixin):

    counselling_date = models.DateField(
        verbose_name='Date of Adherence Counseling',
        blank=True,
        null=True)

    relation = models.CharField(
        verbose_name='Relationship of Adherence Partner to Individual',
        max_length=25,
        default=UNKNOWN,
        choices=RELATIONSHIP)

    relation_other = models.CharField(
        max_length=25,
        verbose_name='If \'Other\', please specify',
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'ba_namotswe'
