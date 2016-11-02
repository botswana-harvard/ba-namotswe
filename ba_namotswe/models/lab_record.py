from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from edc_base.model.validators.date import date_not_future
from edc_lab.choices import UNITS

from ..choices import UTEST_IDS, QUANTIFIERS

from .crf_model_mixin import CrfModelMixin, CrfInlineModelMixin


class LabRecord(CrfModelMixin):
    """A model completed by the user of lab record or assessments."""

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    history = HistoricalRecords()

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
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text='Leave blank to use visit date')

    quantifier = models.CharField(
        verbose_name='quantifier',
        max_length=3,
        choices=QUANTIFIERS,
        default='=')

    value = models.CharField(
        max_length=10)

    units = models.CharField(
        max_length=10,
        choices=UNITS,
        null=True,
        editable=False)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if not self.test_date:
            self.test_date = self.lab_record.subject_visit.visit_date
        return super(LabTest, self).save(*args, **kwargs)

    class Meta(CrfInlineModelMixin.Meta):
        app_label = 'ba_namotswe'
        crf_inline_parent = 'lab_record'
        unique_together = (('lab_record', 'utest_id', 'test_date'), )
