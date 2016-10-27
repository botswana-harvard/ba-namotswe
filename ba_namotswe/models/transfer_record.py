from django.db import models

from ..choices import TRANSFER

from .crf_model import CrfModel


class TransferRecord(CrfModel):

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'


class Transfer(models.Model):

    transfer_record = models.ForeignKey(TransferRecord)

    transfer_date = models.DateField()

    transferred_from = models.CharField(
        verbose_name='Transfered from ...',
        max_length=25,
        choices=TRANSFER)

    transfer_from_other = models.CharField(
        max_length=25,
        verbose_name='... from "Other", please specify',
        blank=True,
        null=True)

    transferred_to = models.CharField(
        verbose_name='Transfered to ...',
        max_length=25,
        choices=TRANSFER)

    transfer_to_other = models.CharField(
        max_length=25,
        verbose_name='... to "Other", please specify',
        blank=True,
        null=True)

    transfer_reason = models.TextField(
        verbose_name='Reason',
        max_length=50)

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
