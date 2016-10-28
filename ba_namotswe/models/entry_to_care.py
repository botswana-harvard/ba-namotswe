from django.db import models
from django.utils import timezone

from edc_base.model.validators.date import date_not_future

from edc_constants.choices import YES_NO_UNKNOWN

from ..choices import MATERNAL_ARVS, INFANT_PROPHYLAXIS

from .crf_model import CrfModel
from edc_constants.constants import NOT_APPLICABLE, UNKNOWN
from django.core.validators import MaxValueValidator, MinValueValidator


class EntryToCare(CrfModel):

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    age_at_entry = models.IntegerField(
        editable=False,
        null=True)

    entry_date = models.DateField(
        verbose_name='Date entered into care',
        validators=[date_not_future, ])

    weight_measured = models.CharField(
        verbose_name='Was weight measured at entry?',
        max_length=15,
        default=UNKNOWN,
        choices=YES_NO_UNKNOWN)

    entry_weight = models.DecimalField(
        verbose_name='Weight at entry (kg)',
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(20), MaxValueValidator(136)],
        blank=True,
        null=True,
        help_text='Provide if available.')

    height_measured = models.CharField(
        verbose_name='Was height measured at entry?',
        max_length=15,
        default=UNKNOWN,
        choices=YES_NO_UNKNOWN)

    entry_height = models.DecimalField(
        verbose_name='Height at entry (cm)',
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(100), MaxValueValidator(244)],
        blank=True,
        null=True,
        help_text='Provide if available.')

    hiv_dx_date = models.DateField(
        verbose_name='HIV Diagnosis Date ',
        validators=[date_not_future, ],
        null=True,
        help_text='Provide if available.')

    hiv_dx_date_estimated = models.BooleanField(
        default=False,
        editable=False,
        help_text='If True, using entry date as HIV diagnosis date.')

    art_init_date = models.DateField(
        verbose_name='ART Initiation Date',
        validators=[date_not_future, ],
        null=True,
        blank=True,
        help_text='Provide if available.')

    phiv = models.CharField(
        verbose_name='Was subject "perinatally infected"?',
        max_length=15,
        default=UNKNOWN,
        choices=YES_NO_UNKNOWN,
        help_text="Diagnosis prior to 10 years of age")

    art_preg = models.CharField(
        verbose_name='Did the subject\'s mother receive ARVs during pregnancy?',
        max_length=15,
        default=UNKNOWN,
        choices=YES_NO_UNKNOWN)

    art_preg_type = models.CharField(
        verbose_name='If "Yes", specify the maternal ARVs received during pregnancy:',
        max_length=25,
        choices=MATERNAL_ARVS,
        default=NOT_APPLICABLE)

    art_preg_type_other = models.CharField(
        verbose_name='If "Other" maternal ARVs received during pregnancy, please specify:',
        max_length=25,
        null=True,
        blank=True)

    infant_ppx = models.CharField(
        verbose_name='Did subject receive infant prophylaxis in the 1st month of life?',
        max_length=15,
        default=UNKNOWN,
        choices=YES_NO_UNKNOWN)

    infant_ppx_type = models.CharField(
        verbose_name='If "Yes", specify the infant prophylaxis.',
        max_length=25,
        default=NOT_APPLICABLE,
        choices=INFANT_PROPHYLAXIS)

    comment = models.TextField(
        max_length=150,
        null=True,
        blank=True,
        help_text='DO NOT include any information that could be used to identify the patient.')

    def save(self, *args, **kwargs):
        # self.age_at_entry = formatted_age(self.dob, self.entry_date)
        if not self.entry_date:
            self.entry_date = self.report_datetime.date()
        if not self.hiv_dx_date:
            self.hiv_dx_date = self.entry_date
            self.hiv_dx_date_estimated = True
        super(EntryToCare, self).save(*args, **kwargs)

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
