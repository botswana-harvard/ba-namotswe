from django.db import models
from django.utils import timezone

from edc_base.model.validators.date import date_not_future
from edc_base.utils.age import formatted_age
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_constants.choices import YES_NO, GENDER


class Enrollment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=20)

    initials = models.CharField(max_length=3)

    gender = models.CharField(
        verbose_name="Gender",
        max_length=1,
        choices=GENDER,
        null=True,
        blank=False)

    dob = models.DateField(
        verbose_name=("Date of birth"),
        null=True,
        blank=False,
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

    class Meta:
        app_label = 'ba_namotswe'

    @property
    def age_at_visit(self):
        return formatted_age(self.dob, self.initial_visit_date)
