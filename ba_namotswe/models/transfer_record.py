from django.db import models

from ..choices import TRANSFER

from .crf_model import CrfModel


class TransferRecord(CrfModel):

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'


class Transfer(models.Model):

    transfer_record = models.ForeignKey(TransferRecord)

    transfer_date = models.DateField()

    transfer_from = models.CharField(
        verbose_name='From ...',
        max_length=25,
        choices=TRANSFER)

    transfer_from_other = models.CharField(
        max_length=15,
        verbose_name='... from "Other"',
        blank=True,
        null=True)

    transfer_to = models.CharField(
        verbose_name='To ...',
        max_length=25,
        choices=TRANSFER)

    transfer_to_other = models.CharField(
        max_length=15,
        verbose_name='... to "Other"',
        blank=True,
        null=True)

    reason = models.TextField(
        verbose_name='Reason',
        null=True,
        blank=True)

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
