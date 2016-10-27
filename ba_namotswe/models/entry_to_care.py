from django.db import models
from django.utils import timezone

from edc_base.model.validators.date import date_not_future

from edc_constants.choices import YES_NO_UNKNOWN

from ..choices import MATERNAL_ARVS, INFANT_PROPHYLAXIS

from .crf_model import CrfModel


class EntryToCare(CrfModel):

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    entry_date = models.DateField(
        verbose_name='Date of Initial Clinic Visit / Entry into care',
        validators=[date_not_future, ])

    entry_weight = models.DecimalField(
        verbose_name='Weight at entry (kg)',
        decimal_places=2,
        max_digits=5,
        blank=True,
        null=True,
        help_text='Provide if available.')

    entry_height = models.DecimalField(
        verbose_name='Height at entry (cm)',
        decimal_places=2,
        max_digits=5,
        blank=True,
        null=True,
        help_text='Provide if available.')

    hiv_dx_date = models.DateField(
        verbose_name='HIV Diagnosis Date ',
        validators=[date_not_future, ],
        help_text='Provide if available.')

    hiv_dx_date_estimated = models.BooleanField(
        default=False,
        editable=False,
        help_text='If True, using entry date as HIV diagnosis date.')

    art_init_date = models.DateField(
        verbose_name='ART Initiation Date',
        validators=[date_not_future, ],
        help_text='Provide if available.')

    phiv = models.CharField(
        verbose_name='Is this an individual who was perinatally infected? (Dx. Prior to 10 years of age)',
        max_length=15,
        choices=YES_NO_UNKNOWN)

    art_preg = models.CharField(
        verbose_name='Did the mother of the individual receive antiretrovirals during pregnancy?',
        max_length=15,
        choices=YES_NO_UNKNOWN)

    art_preg_type = models.CharField(
        verbose_name='Please specify maternal antiretrovirals received during pregnancy:',
        max_length=25,
        choices=MATERNAL_ARVS,
        null=True,
        blank=True)

    art_preg_type_other = models.CharField(
        verbose_name='If other maternal antiretrovirals received during pregnancy, please specify:',
        max_length=25,
        null=True,
        blank=True)

    infant_ppx = models.CharField(
        verbose_name='Did the individual receive infant prophylaxis in the 1st month of life?',
        max_length=15,
        choices=YES_NO_UNKNOWN)

    infant_ppx_type = models.CharField(
        verbose_name='Please specify type of infant prophylaxis in the 1st month of life:',
        max_length=25,
        choices=INFANT_PROPHYLAXIS)

    comment = models.TextField(
        max_length=150,
        null=True,
        blank=True,
        help_text='DO NOT include any information that could be used to identify the patient.')

    def save(self, *args, **kwargs):
        if not self.hiv_dx_date:
            self.hiv_dx_date = self.entry_date
            self.hiv_dx_date_estimated = True
        super(EntryToCare, self).save(*args, **kwargs)

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
