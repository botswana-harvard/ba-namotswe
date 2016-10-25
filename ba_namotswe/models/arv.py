from django.db import models

from .crf_model import CrfModel
from ba_namotswe.models.arv_history import ArvHistory


class Arv(models.Model):

    arv = models.ForeignKey(ArvHistory)

    name = models.CharField(max_length=20)

    date_started = models.DateField()

    date_ended = models.DateField()

    reason_for_switching = models.TextField()

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'ARV History'
