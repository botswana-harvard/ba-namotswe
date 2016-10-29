from datetime import date
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_base.model.validators.date import date_not_future
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.constants import ON_STUDY, YES
from edc_metadata.model_mixins import CreatesMetadataModelMixin
from edc_visit_tracking.constants import SCHEDULED, CHART
from edc_visit_tracking.model_mixins import VisitModelMixin, PreviousVisitModelMixin

from .appointment import Appointment


class SubjectVisit(VisitModelMixin, CreatesMetadataModelMixin, RequiresConsentMixin,
                   PreviousVisitModelMixin, BaseUuidModel):

    appointment = models.OneToOneField(Appointment)

    visit_date = models.DateField(
        verbose_name="Visit Date",
        validators=[
            MinValueValidator(date(2001, 1, 1)),
            date_not_future])

    def save(self, *args, **kwargs):
        if not self.id:
            self.report_datetime = timezone.now()
            self.study_status = ON_STUDY
            self.reason = SCHEDULED
            self.require_crfs = YES
            self.info_source = CHART
        super(SubjectVisit, self).save(*args, **kwargs)

    class Meta:
        app_label = 'ba_namotswe'
        consent_model = 'ba_namotswe.subjectconsent'
