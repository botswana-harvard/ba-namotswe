from django.db import models
from django.utils import timezone

from edc_base.model.validators.date import date_not_future

from ..choices import UTEST_IDS, QUANTIFIERS

from .crf_model import CrfModel
from edc_lab.choices import UNITS


class LabRecord(CrfModel):
    """A model completed by the user of lab record or assessments."""

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'


class LabTest(models.Model):
    """Inline model for Lab."""

    lab_record = models.ForeignKey(LabRecord)

    utest_id = models.CharField(
        verbose_name='Test',
        max_length=25,
        choices=UTEST_IDS)

    test_date = models.DateField(
        validators=[date_not_future])

    quantifier = models.CharField(
        verbose_name='quantifier',
        max_length=3,
        choices=QUANTIFIERS,
        default='=')

    value = models.CharField(
        max_length=10)

    units = models.CharField(
        max_length=10,
        choices=UNITS)

    class Meta:
        app_label = 'ba_namotswe'
