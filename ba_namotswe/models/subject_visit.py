from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import CreatesMetadataModelMixin
from edc_visit_tracking.model_mixins import VisitModelMixin, PreviousVisitModelMixin

from .appointment import Appointment
from edc_constants.constants import ON_STUDY, YES
from edc_visit_tracking.constants import SCHEDULED, CHART


class SubjectVisit(VisitModelMixin, CreatesMetadataModelMixin, RequiresConsentMixin,
                   PreviousVisitModelMixin, BaseUuidModel):

    appointment = models.OneToOneField(Appointment)

    def save(self, *args, **kwargs):
        self.study_status = ON_STUDY
        self.reason = SCHEDULED
        self.require_crfs = YES
        self.info_source = CHART
        super(SubjectVisit, self).save(*args, **kwargs)

    class Meta:
        app_label = 'ba_namotswe'
        consent_model = 'ba_namotswe.subjectconsent'
