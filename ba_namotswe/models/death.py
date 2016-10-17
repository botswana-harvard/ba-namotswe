from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel


class Death(BaseUuidModel):

    dod = models.DateField(
        verbose_name='Date of Death',
        blank=True,
        null=True)

    death_cause = models.CharField(
        max_length=25,
        verbose_name='Cause of Death',
        blank=True,
        null=True)

    def __str__(self):
        return self.display_name

    class Meta:
        app_label = 'ba_namotswe'
