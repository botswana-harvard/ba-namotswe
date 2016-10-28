from django.db import models
from django.urls import reverse

from edc_base.model.models import BaseUuidModel
from edc_visit_tracking.model_mixins import CrfModelMixin

from .subject_visit import SubjectVisit
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from django.utils import timezone
from edc_base.model.models.url_mixin import UrlMixin
from edc_constants.constants import UNKNOWN
from django.utils.html import format_html

REPORT_STATUS = (
    ('REMIND', 'Remind'),
    ('NOT_AVAILABLE', 'Not available'),
    ('INCOMPLETE', 'Incomplete')
)


class CrfModel(CrfModelMixin, UrlMixin, RequiresConsentMixin, UpdatesCrfMetadataModelMixin, BaseUuidModel):

    """ Base model for all CRFs. """

    ADMIN_SITE_NAME = 'ba_namotswe_admin'

    subject_visit = models.OneToOneField(SubjectVisit)

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    edited = models.BooleanField(default=False, editable=False)

    flagged = models.BooleanField(default=False, editable=False)

    flagged_datetime = models.DateTimeField(null=True, editable=False)

    reviewed = models.BooleanField(default=False, editable=False)

    reviewed_datetime = models.DateTimeField(null=True, editable=False)

    pending_fields = models.TextField(verbose_name='Pending', null=True, editable=False)

    dashboard_comment = models.CharField(max_length=50, null=True, editable=False)

    def __str__(self):
        return str(self.subject_visit)

    def save(self, *args, **kwargs):
        if not kwargs.get('update_fields'):
            self.edited = True
            self.pending_fields = ', '.join(self.get_pending_fields())
        super(CrfModel, self).save(*args, **kwargs)

    @property
    def subject_identifier(self):
        return self.subject_visit.subject_identifier

    @property
    def visit_code(self):
        return self.subject_visit.visit_code

    def get_absolute_url(self):
        if self.id:
            return reverse(
                'ba_namotswe_admin:{}_{}_change'.format(*self._meta.label_lower.split('.')), args=(str(self.id), ))
        else:
            return reverse('ba_namotswe_admin:{}_{}_add'.format(*self._meta.label_lower.split('.')))

    def dashboard(self):
        """Returns a hyperink for the Admin page."""
        url = reverse(
            'subject_dashboard_url',
            kwargs={
                'subject_identifier': self.subject_visit.subject_identifier,
                'appointment_pk': str(self.subject_visit.appointment.pk),
            })
        ret = """<a href="{url}" role="button" class="btn btn-sm btn-primary">dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    def get_pending_fields(self):
        pending_fields = []
        for key, value in self.__dict__.items():
            if value == UNKNOWN:
                pending_fields.append(key)
        pending_fields.sort()
        return pending_fields

    class Meta:
        consent_model = 'ba_namotswe.subjectconsent'
        abstract = True
