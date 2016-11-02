from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from ..constants import RESOLVED
from ..choices import OI_STATUS, OI_OPTIONS

from .crf_model_mixin import CrfModelMixin, CrfInlineModelMixin


class OiRecord(CrfModelMixin):

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Opportunistic Infection'
        verbose_name_plural = 'Opportunistic Infections'


class Oi(CrfInlineModelMixin):

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

    history = HistoricalRecords()

    def __str__(self):
        return self.oi

    class Meta(CrfInlineModelMixin.Meta):
        app_label = 'ba_namotswe'
        crf_inline_parent = 'oi_record'
