from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from edc_constants.choices import YES_NO_UNKNOWN, YES_NO_UNKNOWN_NA
from edc_constants.constants import UNKNOWN

from .crf_model_mixin import CrfModelMixin


class InCare(CrfModelMixin):

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    weight_measured = models.CharField(
        verbose_name='Was weight measured?',
        max_length=15,
        default=UNKNOWN,
        choices=YES_NO_UNKNOWN)

    weight = models.DecimalField(
        verbose_name='Weight (kg)',
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(20), MaxValueValidator(136)],
        blank=True,
        null=True,
        help_text='Provide if available.')

    height_measured = models.CharField(
        verbose_name='Was height measured?',
        max_length=15,
        default=UNKNOWN,
        choices=YES_NO_UNKNOWN)

    height = models.DecimalField(
        verbose_name='Height (cm)',
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(100), MaxValueValidator(244)],
        blank=True,
        null=True,
        help_text='Provide if available.')

    hospital = models.CharField(
        verbose_name='Has the patient been hospitalized since last visit?',
        max_length=15,
        default=UNKNOWN,
        choices=YES_NO_UNKNOWN)

    hospital_date = models.DateField(
        verbose_name='Date hospitalized',
        null=True,
        blank=True)

    hospital_reason = models.TextField(
        verbose_name='Reason for patient was hospitalized',
        null=True,
        blank=True)

    disclosure_to_patient = models.CharField(
        verbose_name='Evidence of disclosure of HIV status to patient?',
        max_length=15,
        default=UNKNOWN,
        choices=YES_NO_UNKNOWN,
        help_text=(
            'If <= 18 years, Is there evidence that disclosure has been made '
            'to the youth/adolescent that they are HIV-infected?'))

    disclosure_to_patient_date = models.DateField(
        verbose_name='Date of disclosure to patient',
        null=True,
        blank=True)

    disclosure_to_others = models.CharField(
        verbose_name='Evidence of disclosure of HIV status by patient to others?',
        max_length=15,
        default=UNKNOWN,
        choices=YES_NO_UNKNOWN,
        help_text=(
            'Is there evidence that the patient has disclosed his/her HIV status to others?'))

    disclosure_to_others_date = models.DateField(
        verbose_name='Date of disclosure to others',
        null=True,
        blank=True)

    disclosure_by_caregiver = models.CharField(
        verbose_name='Evidence of disclosure of HIV status by caregiver?',
        max_length=15,
        default=UNKNOWN,
        choices=YES_NO_UNKNOWN_NA,
        help_text=(
            'If <= 18 years, is there evidence that the caregiver has disclosed the patient\'s HIV status to others?'))

    class Meta(CrfModelMixin.Meta):
        app_label = 'ba_namotswe'
