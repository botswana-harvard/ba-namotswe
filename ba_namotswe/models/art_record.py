from django.db import models
from django.utils import timezone

from edc_constants.constants import OTHER

from .crf_model import CrfModel

REASON_STOPPED_CHOICES = (
    ('REASON1', 'Reason 1'),
    ('REASON2', 'Reason 2'),
    ('REASON3', 'Reason 3'),
    (OTHER, 'Other, specify ...')
)


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

    name = models.CharField(
        max_length=25,
        help_text='Use 3 letter abbrev separated by commas.')

    regimen = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    date_started = models.DateField()

    date_stopped = models.DateField(
        null=True,
        blank=True)

    is_ongoing = models.BooleanField(default=False)

    reason_ended = models.CharField(
        max_length=50,
        choices=REASON_STOPPED_CHOICES)

    reason_ended_other = models.TextField(
        max_length=50,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        # self.regimen = self.parse_regimen(self.name)
        super(ArtRegimen, self).save(*args, **kwargs)

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'ART Regimen'
