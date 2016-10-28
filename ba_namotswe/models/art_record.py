from django.db import models
from django.utils import timezone

from ..choices import ART_STATUS

from .crf_model import CrfModel
from ba_namotswe.constants import ONGOING
from ba_namotswe.choices import ART_REGIMENS


class ArtRecord(CrfModel):

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    comment = models.TextField(
        max_length=250,
        null=True,
        blank=True)

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'ART Record'


class ArtRegimen(models.Model):

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

    comment = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        # self.regimen = self.parse_regimen(self.name)
        super(ArtRegimen, self).save(*args, **kwargs)

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'ART Regimen'
