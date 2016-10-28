from django.db import models
from django.utils import timezone

from ..choices import OI_OPTIONS

from .crf_model import CrfModel
from ba_namotswe.constants import ONGOING, RESOLVED
from ba_namotswe.choices import OI_STATUS


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

    oi = models.CharField(
        max_length=200,
        choices=OI_OPTIONS)

    started = models.DateField()

    stopped = models.DateField(
        blank=True,
        null=True)

    status = models.CharField(
        max_length=15,
        default=RESOLVED,
        choices=OI_STATUS)

    def __str__(self):
        return self.oi

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
