from django.db import models

from .crf_model import CrfModel
from ..choices import OI_OPTIONS


class Oi(CrfModel):

    oi_type = models.CharField(
        max_length=200,
        choices=OI_OPTIONS)

    def __str__(self):
        return self.oi_type

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
