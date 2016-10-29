from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from edc_base.model.models import BaseUuidModel
from edc_visit_tracking.model_mixins import (
    CrfModelMixin as VisitTrackingCrfModelMixin,
    CrfInlineModelMixin as VisitTrackingCrfInlineModelMixin)

from edc_base.model.models.url_mixin import UrlMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_constants.constants import UNKNOWN
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin

from .subject_visit import SubjectVisit

REPORT_STATUS = (
    ('REMIND', 'Remind'),
    ('NOT_AVAILABLE', 'Not available'),
    ('INCOMPLETE', 'Incomplete')
)


class DashboardMixin(models.Model):

    def dashboard(self):
        """Returns a hyperink for the Admin page."""
        url = reverse(
            'subject_dashboard_url',
            kwargs={
                'subject_identifier': self.subject_identifier,
                'appointment_pk': str(self.appointment.pk),
            })
        ret = """<a href="{url}" role="button" class="btn btn-sm btn-primary">dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    class Meta:
        abstract = True


class PendingFieldsMixin(models.Model):

    pending_fields = models.TextField(verbose_name='Pending', null=True, editable=False)

    def save(self, *args, **kwargs):
        if not kwargs.get('update_fields'):
            self.pending_fields = ', '.join(self.get_pending_fields())
        super(PendingFieldsMixin, self).save(*args, **kwargs)

    def get_pending_fields(self):
        pending_fields = []
        for key, value in self.__dict__.items():
            if value == UNKNOWN:
                pending_fields.append(key)
        pending_fields.sort()
        return pending_fields

    class Meta:
        abstract = True


class ReviewFieldsMixin(models.Model):

    edited = models.BooleanField(default=False, editable=False)

    flagged = models.BooleanField(default=False, editable=False)

    flagged_datetime = models.DateTimeField(null=True, editable=False)

    reviewed = models.BooleanField(default=False, editable=False)

    reviewed_datetime = models.DateTimeField(null=True, editable=False)

    no_report = models.BooleanField(default=False, editable=False)

    no_report_datetime = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        if not kwargs.get('update_fields'):
            self.edited = True
            self.no_report = False
            self.no_report_datetime = None
        super(ReviewFieldsMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class CrfInlineModelMixin(DashboardMixin, VisitTrackingCrfInlineModelMixin, ReviewFieldsMixin, UrlMixin,
                          PendingFieldsMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'ba_namotswe_admin'

    @property
    def appointment(self):
        return self.visit.appointment

    @property
    def visit_code(self):
        return self.visit.visit_code

    class Meta:
        abstract = True


class CrfModelMixin(DashboardMixin, VisitTrackingCrfModelMixin, ReviewFieldsMixin, UrlMixin, RequiresConsentMixin,
                    UpdatesCrfMetadataModelMixin, PendingFieldsMixin, BaseUuidModel):

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
            lfu = LostToFollowup.objects.get(subject_identifier=self.subject_identifier)
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
