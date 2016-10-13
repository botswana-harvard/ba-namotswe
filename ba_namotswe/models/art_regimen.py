from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel


class ARTRegimen(BaseUuidModel):

    name = models.CharField(max_length=10)

    display_name = models.CharField(max_length=25)

    def __str__(self):
        return self.display_name

    class Meta:
        app_label = 'ba_namotswe'
