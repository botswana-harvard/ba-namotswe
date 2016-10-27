from django.db import models

from .crf_model import CrfModel


class PregnancyHistory(CrfModel):

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Pregnancy History'
        verbose_name_plural = 'Pregnancy History'


class Pregnancy(models.Model):

    pregnancy_history = models.ForeignKey(PregnancyHistory)

    pregnancy_date = models.DateField(
        verbose_name='Date of first clinical documentation of pregnancy')

    delivery_date = models.DateField()

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Pregnancy'
