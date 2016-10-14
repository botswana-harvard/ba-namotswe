from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel


class TransferHistory(BaseUuidModel):

    transfer_details = models.CharField(
        verbose_name="Transfer of Care Details",
        max_length=15,
        choices=('date_of_transfer', 'Date of Transfer'),
                ('reason_for_transfer', 'Reason for Transfer')),

    transfer_loc = models.CharField(
        verbose_name='Location of transfer',
        max_length=25,
        blank=True,
        default=None,
        choices=(
            ('into_idcc', 'Into IDCC')
            ('out_of_idcc', 'Out of IDCC'),
            ('into private_clinic', 'Into Private Clinic'),
            ('out_of_private_clinic', 'Out of Private Clinic'),
            ('into_bipai', 'Into BIPAI'),
            ('out_of_bipai', 'Out of BIPAI'),
            ('OTHER', 'Other, specify')),

    transfer_loc_other = models.CharField(
        max_length=25,
        verbose_name='location of transfer: "Other"',
        blank=True,
        null=True)

     def __str__(self):
        return self.display_name

    class Meta:
        app_label = 'ba_namotswe'