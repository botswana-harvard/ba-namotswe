from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from edc_base.model.models import BaseUuidModel, UrlMixin

from ..model_mixins import DashboardModelMixin


class Death(DashboardModelMixin, UrlMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'ba_namotswe_admin'

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        unique=True)

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    death_date = models.DateField(
        verbose_name='Date of Death',
        blank=True,
        null=True)

    death_cause = models.CharField(
        max_length=25,
        verbose_name='Cause of Death',
        blank=True,
        null=True)

    objects = models.Manager()

    history = HistoricalRecords()

    class Meta:
        app_label = 'ba_namotswe'
