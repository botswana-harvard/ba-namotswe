from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings

from edc_base.model.validators.date import date_not_future
from edc_base.utils.age import formatted_age
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_constants.choices import YES_NO, GENDER

from .subject_consent import SubjectConsent


class Enrollment(CreateAppointmentsMixin, BaseUuidModel):

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        editable=False)

    study_site = models.CharField(
        max_length=10,
        default=settings.STUDY_SITE,
        editable=False)

    initials = models.CharField(max_length=3)

    gender = models.CharField(
        verbose_name="Gender",
        max_length=1,
        choices=GENDER)

    dob = models.DateField(
        verbose_name=("Date of birth"),
        help_text=("Format is YYYY-MM-DD"))

    report_datetime = models.DateTimeField(default=timezone.now)

    is_eligible = models.BooleanField(default=True)

    initial_visit_date = models.DateField(
        verbose_name='Date of Initial Clinic Visit',
        validators=[date_not_future, ])

    # TODO: skip_logic caregiver_relation: display field only if 10 years ago _ DOB _ 13 years ago? (adolescents only--ASK AT SLH)
    caregiver_relation = models.CharField(
        verbose_name='Caregiver/Next of Kin Relationship',
        max_length=25,
        blank=True,
        default=None,
        choices=(
            ('mother', 'Mother'),
            ('father', 'Father'),
            ('grandmother', 'Grandmother'),
            ('grandfather', 'Grandfather'),
            ('aunt', 'Aunt'),
            ('uncle', 'Uncle'),
            ('legal_guardian', 'Legal Guardian'),
            ('not_applicable', 'Not Applicable'),
            ('OTHER', 'Other, specify')),
        help_text='Please describe the caregiver/next of kin\'s relationship to patient')

    # TODO: skip_logic caregiver_relation_other: display field only if Caregiver/Next of Kin Relationship= OTHER
    caregiver_relation_other = models.CharField(
        max_length=25,
        verbose_name='Caregiver/Next of Kin Relationship: "Other"',
        blank=True,
        null=True)

    weight_measured = models.CharField(
        max_length=25,
        verbose_name='Weight was measured at Initial Clinic Visit',
        choices=YES_NO)

    weight = models.DecimalField(
        verbose_name='Weight in kg',
        decimal_places=2,
        max_digits=5,
        blank=True,
        null=True)

    height_measured = models.CharField(
        max_length=25,
        verbose_name='Height was measured at Initial Clinic Visit',
        choices=YES_NO)

    height = models.DecimalField(
        verbose_name='Height in cm',
        decimal_places=2,
        max_digits=5,
        blank=True,
        null=True)

    hiv_diagnosis_date = models.DateField(
        verbose_name='HIV Diagnosis Date ',
        validators=[date_not_future, ],
        blank=True,
        null=True,
        help_text='Leave blank if diagnosis date is same as initial visit date')

    art_initiation_date = models.DateField(
        verbose_name='ART Initiation Date',
        validators=[date_not_future, ])

    def save(self, *args, **kwargs):
        if not self.hiv_diagnosis_date:
            self.hiv_diagnosis_date = self.initial_visit_date
        super(Enrollment, self).save(*args, **kwargs)

    @property
    def age_at_visit(self):
        return formatted_age(self.dob, self.initial_visit_date)

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
        print('subject={}'.format(self.subject_identifier))
        url = reverse(
            'subject_dashboard_url',
            kwargs={
                'subject_identifier': self.subject_identifier
            })
        ret = """<a href="{url}" >dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    class Meta:
        app_label = 'ba_namotswe'
        consent_model = 'ba_namotswe.subjectconsent'
        visit_schedule_name = 'visit_schedule'
