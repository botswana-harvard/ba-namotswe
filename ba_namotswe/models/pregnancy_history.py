from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel


PREGNANCY = (
    ('date_of_first_clinical_documentation_of_pregnancy', 'Date of First Clinical Documentation of Pregnancy'),
    ('date_of_delivery', 'Date of Delivery'),)


class PregnancyHistory(BaseUuidModel):

    class Meta:
        app_label = 'ba_namotswe'

    pregnancy_details = models.CharField(
        max_length=7,
        verbose_name='Has the participant moved out of the household where last seen',
        choices=PREGNANCY,
        null=True,
        blank=False,
        help_text="")
