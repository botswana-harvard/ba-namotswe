from django.db import models

from simple_history.models import HistoricalRecords

from edc_constants.constants import UNKNOWN

from ..choices import RELATIONSHIP

from .crf_model_mixin import CrfModelMixin


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

    history = HistoricalRecords()

    objects = models.Manager()

    def get_pending_fields(self):
        pending_fields = super(AdherenceCounselling, self).get_pending_fields()
        if not self.counselling_date:
            pending_fields.append('counselling_date')
        pending_fields.sort()
        return pending_fields

    class Meta(CrfModelMixin.Meta):
        app_label = 'ba_namotswe'
