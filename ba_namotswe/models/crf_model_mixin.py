from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from edc_visit_tracking.model_mixins import (
    CrfModelMixin as VisitTrackingCrfModelMixin, CrfInlineModelMixin as VisitTrackingCrfInlineModelMixin)

from ..model_mixins import DashboardModelMixin, PendingFieldsModelMixin, ReviewFieldsModelMixin

from .subject_visit import SubjectVisit
from edc_visit_tracking.managers import CrfModelManager


class CrfInlineModelMixin(DashboardModelMixin, VisitTrackingCrfInlineModelMixin, ReviewFieldsModelMixin, UrlMixin,
                          PendingFieldsModelMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'ba_namotswe_admin'

    @property
    def appointment(self):
        return getattr(self, self._meta.crf_inline_parent).visit.appointment

    @property
    def visit_code(self):
        return self.appointment.visit_code

    class Meta:
        abstract = True


class CrfModelMixin(DashboardModelMixin, VisitTrackingCrfModelMixin, ReviewFieldsModelMixin, UrlMixin,
                    RequiresConsentMixin, UpdatesCrfMetadataModelMixin, PendingFieldsModelMixin, BaseUuidModel):

    """ Base model for all CRFs. """

    ADMIN_SITE_NAME = 'ba_namotswe_admin'

    subject_visit = models.OneToOneField(SubjectVisit)

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    dashboard_comment = models.CharField(max_length=50, null=True, editable=False)

    comment = models.TextField(
        max_length=150,
        null=True,
        blank=True,
        help_text='DO NOT include any information that could be used to identify the patient.')

    def __str__(self):
        return str(self.subject_visit)

    def save(self, *args, **kwargs):
        try:
            LostToFollowup = django_apps.get_model(self._meta.app_label, 'losttofollowup')
            lfu = LostToFollowup.objects.get(subject_identifier=self.get_subject_identifier())
            if lfu.last_contact_date < self.subject_visit.visit_date:
                raise ValidationError('Subject was report LFU on {}'.format(lfu.last_contact_date))
        except LostToFollowup.DoesNotExist:
            pass
        super(CrfModelMixin, self).save(*args, **kwargs)

    @property
    def appointment(self):
        return self.visit.appointment

    @property
    def subject_identifier(self):
        return self.get_subject_identifier()

    class Meta(VisitTrackingCrfModelMixin.Meta):
        consent_model = 'ba_namotswe.subjectconsent'
        abstract = True
