from django.db import models
from django.utils import timezone

from ..choices import OI_OPTIONS

from .crf_model import CrfModel


class OiRecord(CrfModel):

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    comment = models.TextField(
        max_length=250,
        null=True,
        blank=True)

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Opportunistic Infection'
        verbose_name_plural = 'Opportunistic Infections'


class Oi(models.Model):

    oi_record = models.ForeignKey(OiRecord)

    oi_type = models.CharField(
        max_length=200,
        choices=OI_OPTIONS)

    start_date = models.DateField()

    stop_date = models.DateField(
        blank=True,
        null=True)

    is_ongoing = models.BooleanField(default=False)

    def __str__(self):
        return self.oi_type

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
