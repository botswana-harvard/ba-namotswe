from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_metadata.model_mixins import CreatesMetadataModelMixin
from edc_visit_tracking.model_mixins import VisitModelMixin, PreviousVisitModelMixin

from .appointment import Appointment


class SubjectVisit(VisitModelMixin, CreatesMetadataModelMixin, PreviousVisitModelMixin, BaseUuidModel):

    appointment = models.OneToOneField(Appointment)

    class Meta:
        app_label = 'ba_namotswe'
