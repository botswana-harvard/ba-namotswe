from django.db import models

from .crf_model import CrfModel


class ArtRegimen(CrfModel):

    name = models.CharField(max_length=10)

    display_name = models.CharField(max_length=25)

    def __str__(self):
        return self.display_name

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
