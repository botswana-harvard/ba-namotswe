from django.db import models

from simple_history.models import HistoricalRecords

from edc_base.model.validators.date import date_not_future

from ..choices import TB_TYPE, TEST_TYPE

from .crf_model_mixin import CrfModelMixin, CrfInlineModelMixin


class TbRecord(CrfModelMixin):

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Tuberculosis Infection History'
        verbose_name_plural = 'Tuberculosis Infection History'


class Tb(CrfInlineModelMixin):

    tb_record = models.ForeignKey(TbRecord)

    dx_date = models.DateField(
        verbose_name='Date of diagnosis',
        validators=[date_not_future, ])

    tb_type = models.CharField(
        verbose_name='TB type',
        max_length=30,
        choices=TB_TYPE)

    dx_method = models.CharField(
        verbose_name='Diagnosis method',
        max_length=30,
        choices=TEST_TYPE)

    dx_method_other = models.CharField(
        verbose_name='If \'Other\', specify',
        blank=True,
        null=True,
        max_length=50)

    history = HistoricalRecords()

    class Meta(CrfInlineModelMixin.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'TB History'
        crf_inline_parent = 'tb_record'
