from django.db import models
from django.utils import timezone

from edc_base.model.validators.date import date_not_future
from edc_lab.choices import UNITS

from ..choices import UTEST_IDS, QUANTIFIERS

from .crf_model_mixin import CrfModelMixin, CrfInlineModelMixin


class LabRecord(CrfModelMixin):
    """A model completed by the user of lab record or assessments."""

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    class Meta(CrfModelMixin.Meta):
        app_label = 'ba_namotswe'


class LabTest(CrfInlineModelMixin):
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

    class Meta(CrfInlineModelMixin.Meta):
        app_label = 'ba_namotswe'
        crf_inline_parent = 'lab_record'
