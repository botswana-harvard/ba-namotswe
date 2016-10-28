from uuid import uuid4

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_base.utils.age import formatted_age
from edc_constants.choices import GENDER

from ..choices import RELATIONSHIP

from .subject_consent import SubjectConsent
from edc_base.model.models.url_mixin import UrlMixin


def get_uuid():
    return str(uuid4())


class Enrollment(CreateAppointmentsMixin, UrlMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'ba_namotswe_admin'

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        unique=True,
        default=get_uuid,
        editable=False)

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    study_site = models.CharField(
        max_length=10,
        default=settings.STUDY_SITE,
        editable=False)

    slh_identifier = models.CharField(
        verbose_name='SLH Number',
        max_length=25,
        unique=True)

    cm_identifier = models.CharField(
        verbose_name='CM Number',
        max_length=25,
        blank=True,
        null=True,
        help_text='Provide if available.')

    initials = models.CharField(max_length=3, null=True, blank=True)

    gender = models.CharField(
        verbose_name="Gender",
        max_length=1,
        choices=GENDER)

    dob = models.DateField(
        verbose_name=("Date of birth"),
        help_text=("Format is YYYY-MM-DD"))

    # TODO: skip_logic caregiver_relation: display field only if 10 years ago _ DOB _ 13 years ago? (adolescents only--ASK AT SLH)
    caregiver_relation = models.CharField(
        verbose_name='Caregiver/Next of Kin Relationship',
        max_length=25,
        blank=True,
        null=True,
        choices=RELATIONSHIP,
        help_text='Required if 10-13 years old, otherwise leave blank.')

    # TODO: skip_logic caregiver_relation_other: display field only if Caregiver/Next of Kin Relationship= OTHER
    caregiver_relation_other = models.CharField(
        max_length=25,
        verbose_name='Caregiver/Next of Kin Relationship: "Other"',
        blank=True,
        null=True)

    def age(self):
        return formatted_age(self.dob, timezone.now().date())
    age.allow_tags = True

    @property
    def subject_consent(self):
        try:
            subject_consent = SubjectConsent.objects.get(
                subject_identifier=self.subject_identifier,
                study_site='')
        except SubjectConsent.DoesNotExist:
            subject_consent = SubjectConsent.objects.create(
                consent_datetime=self.report_datetime,
                dob=self.dob,
                gender=self.gender,
                initials=self.initials,
                study_site=self.study_site,
            )
        return subject_consent

    def dashboard(self):
        """Returns a hyperink for the Admin page."""
        url = reverse(
            'subject_dashboard_url',
            kwargs={
                'subject_identifier': self.subject_identifier
            })
        ret = """<a href="{url}" role="button" class="btn btn-sm btn-primary">dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    class Meta:
        app_label = 'ba_namotswe'
        consent_model = 'ba_namotswe.subjectconsent'
        visit_schedule_name = 'visit_schedule'
        verbose_name = 'Enrollment'
