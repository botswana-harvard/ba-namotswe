from django.db import models
from django.utils import timezone

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_metadata.model_mixins import CreatesMetadataModelMixin, UpdateCrfMetadataModelMixin
from edc_registration.model_mixins import RegisteredSubjectModelMixin, RegisteredSubjectMixin
from edc_visit_tracking.model_mixins import VisitModelMixin, PreviousVisitModelMixin, CrfModelMixin


class RegisteredSubject(RegisteredSubjectModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'banamotswe'


class Enrollment(RegisteredSubjectMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(default=timezone.now)

    is_eligible = models.BooleanField(default=True)

    class Meta:
        app_label = 'banamotswe'


class SubjectVisit(VisitModelMixin, CreatesMetadataModelMixin, PreviousVisitModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'banamotswe'


class CrfOne(CrfModelMixin, UpdateCrfMetadataModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    f1 = models.CharField(max_length=10, default='erik')

    class Meta:
        app_label = 'banamotswe'
