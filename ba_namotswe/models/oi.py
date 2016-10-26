from django.db import models

from .crf_model import CrfModel
from ..choices import OI_OPTIONS
from ba_namotswe.models.oi_history import OiHistory


class Oi(models.Model):

    oi = models.ForeignKey(OiHistory)

    oi_type = models.CharField(
        max_length=200,
        choices=OI_OPTIONS)

    date_of_infection = models.DateField()

    date_infection_ended = models.DateField(
        blank=True,
        null=True)

    def __str__(self):
        return self.oi_type

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
