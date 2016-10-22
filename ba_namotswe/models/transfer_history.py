from django.db import models

from .crf_model import CrfModel
from ..choices import TRANSFER


class TransferHistory(CrfModel):

    transfer_details = models.CharField(
        verbose_name="Transfer of Care Details",
        max_length=15,
        choices=(
            ('date_of_transfer', 'Date of Transfer'),
            ('reason_for_transfer', 'Reason for Transfer'))
    )

    transfer_loc = models.CharField(
        verbose_name='Location of transfer',
        max_length=25,
        blank=True,
        default=None,
        choices=TRANSFER)

    transfer_loc_other = models.CharField(
        max_length=25,
        verbose_name='location of transfer: "Other"',
        blank=True,
        null=True)

    def __str__(self):
        return self.display_name

    class Meta:
        app_label = 'ba_namotswe'
