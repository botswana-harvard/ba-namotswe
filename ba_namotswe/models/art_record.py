from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from ..choices import ART_STATUS, ART_REGIMENS
from ..constants import ONGOING

from .crf_model_mixin import CrfModelMixin, CrfInlineModelMixin


class ArtRecord(CrfModelMixin):

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'ART Record'


class ArtRegimen(CrfInlineModelMixin, models.Model):

    art_record = models.ForeignKey(ArtRecord)

    regimen = models.CharField(
        max_length=25,
        choices=ART_REGIMENS)

    started = models.DateField(
        null=True,
        blank=True)

    stopped = models.DateField(
        verbose_name='Stopped/Held',
        null=True,
        blank=True)

    status = models.CharField(
        max_length=50,
        default=ONGOING,
        choices=ART_STATUS)

    reason = models.CharField(max_length=25, null=True, blank=True)

    history = HistoricalRecords()

    objects = models.Manager()

    class Meta(CrfInlineModelMixin.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'ART Regimen'
        crf_inline_parent = 'art_record'
