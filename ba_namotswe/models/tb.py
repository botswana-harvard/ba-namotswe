from django.db import models

from edc_base.model.validators.date import date_not_future

from .crf_model import CrfModel
from ..choices import TB_TYPE, TEST_TYPE
from ba_namotswe.models.tb_history import TbHistory


class Tb(models.Model):

    tb = models.ForeignKey(TbHistory)

    tb_date = models.DateField(
        verbose_name='Date of TB diagnosis',
        validators=[date_not_future, ])

    tb_type = models.CharField(
        verbose_name='Type of TB',
        max_length=30,
        choices=TB_TYPE)

    tb_test = models.CharField(
        verbose_name='Method of TB diagnosis',
        max_length=30,
        choices=TEST_TYPE)

    tb_test_other = models.CharField(
        verbose_name='Method of TB diagnosis: Other',
        blank=True,
        null=True,
        max_length=50)

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'ARV History'
