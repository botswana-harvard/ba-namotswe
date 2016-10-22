from django.db import models

from edc_base.model.validators.date import date_not_future

from .crf_model import CrfModel
from ..choices import TB_TYPE, TEST_TYPE


class TbHistory(CrfModel):

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
