from dateutil.relativedelta import relativedelta
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_base.model.models.url_mixin import UrlMixin
from edc_base.utils.age import formatted_age
from edc_constants.choices import GENDER, YES_NO
from edc_constants.constants import UNKNOWN, YES

from ..choices import RELATIONSHIP

from .subject_consent import SubjectConsent


def get_uuid():
    return str(uuid4())


def validate_dob(value):
    if value:
        age_in_years = relativedelta(timezone.now().date(), value).years
        if age_in_years <= 10:
            raise ValidationError(
                _('Ensure age is greater than or equal to 10 years old. Got %(age_in_years)s.'),
                params={'age_in_years': age_in_years},
            )
        if age_in_years >= 35:
            raise ValidationError(
                _('Ensure age is less than or equal to 35 years old. Got %(age_in_years)s.'),
                params={'age_in_years': age_in_years},
            )


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

    entry_to_care = models.CharField(
        verbose_name='Patient entered into care on or after 1 Jan 2001?',
        max_length=10,
        choices=YES_NO,
        validators=[RegexValidator('^' + YES + '$', message='Patient is not eligible for enrollment.')])

    initiation = models.CharField(
        verbose_name='Patient initiated ART on or before 1 June 2016?',
        max_length=10,
        choices=YES_NO,
        validators=[RegexValidator('^' + YES + '$', message='Patient is not eligible for enrollment.')])

    gender = models.CharField(
        verbose_name="Gender",
        max_length=1,
        choices=GENDER)

    dob = models.DateField(
        verbose_name=("Date of birth"),
        validators=[validate_dob],
        help_text=("Format is YYYY-MM-DD"))

    caregiver_relation = models.CharField(
        verbose_name='Caregiver/Next of Kin Relationship',
        max_length=25,
        default=UNKNOWN,
        choices=RELATIONSHIP)

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
