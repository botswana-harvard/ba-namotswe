from django.db import models
from django.urls import reverse

from edc_base.model.models import BaseUuidModel
from edc_visit_tracking.model_mixins import CrfModelMixin

from .subject_visit import SubjectVisit
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from django.utils import timezone

REPORT_STATUS = (
    ('REMIND', 'Remind'),
    ('NOT_AVAILABLE', 'Not available'),
    ('INCOMPLETE', 'Incomplete')
)


class CrfModel(CrfModelMixin, RequiresConsentMixin, UpdatesCrfMetadataModelMixin, BaseUuidModel):

    """ Base model for all CRFs. """

    subject_visit = models.OneToOneField(SubjectVisit)

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    edited = models.BooleanField(default=False, editable=False)

    flagged = models.BooleanField(default=False, editable=False)

    flagged_datetime = models.DateTimeField(null=True, editable=False)

    reviewed = models.BooleanField(default=False, editable=False)

    reviewed_datetime = models.DateTimeField(null=True, editable=False)

    dashboard_comment = models.CharField(max_length=50, null=True, editable=False)

    def save(self, *args, **kwargs):
        if not kwargs.get('update_fields'):
            self.edited = True
        super(CrfModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.id:
            return reverse(
                'ba_namotswe_admin:{}_{}_change'.format(*self._meta.label_lower.split('.')), args=[str(self.id)])
        else:
            return reverse('ba_namotswe_admin:{}_{}_add'.format(*self._meta.label_lower.split('.')))

    class Meta:
        consent_model = 'ba_namotswe.subjectconsent'
        abstract = True
