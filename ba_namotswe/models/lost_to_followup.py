from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from edc_base.model.models import BaseUuidModel, UrlMixin

from ..model_mixins import DashboardModelMixin


class LostToFollowup(DashboardModelMixin, UrlMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'ba_namotswe_admin'

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        unique=True)

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    last_contact_date = models.DateField()

    last_visit_date = models.DateField()

    history = HistoricalRecords()

    class Meta:
        app_label = 'ba_namotswe'
