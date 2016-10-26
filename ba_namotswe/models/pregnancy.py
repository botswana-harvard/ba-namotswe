from django.db import models

from .crf_model import CrfModel

from ba_namotswe.models.pregnancy_history import PregnancyHistory


class Pregnancy(models.Model):

    pregnancy = models.ForeignKey(PregnancyHistory)

    date_of_documentation = models.DateField(
        verbose_name='Date of first clinical documentation of pregnancy')

    date_of_delivery = models.DateField()

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Pregnancy History'