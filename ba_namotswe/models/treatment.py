from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_constants.choices import YES_NO_UNKNOWN
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from edc_visit_tracking.model_mixins import CrfModelMixin

from .art_regimen import ARTRegimen


class Treatment(CrfModelMixin, UpdatesCrfMetadataModelMixin, BaseUuidModel):

    perinatal_infection = models.CharField(
        max_length=25,
        verbose_name='Is this an individual who was perinatally infected? (Dx. Prior to 10 years of age)',
        choices=YES_NO_UNKNOWN)

    # TODO: skip_logic pmtct: display field only if perinatally infected= YES
    pmtct = models.CharField(
        max_length=25,
        verbose_name='Did the mother of the individual receive antiretrovirals during pregnancy?',
        choices=YES_NO_UNKNOWN,
        blank=True,
        null=True)

    # TODO: skip_logic pmtct_rx: display field only if antiretrovirals in pregnancy=YES
    pmtct_rx = models.CharField(
        max_length=25,
        verbose_name='Please specify type of antiretrovirals received during pregnancy: ',
        choices=(('azt_monotherapy', 'AZT Monotherapy'), ('dsnvp', 'dsNVP'), ('triple_arv', 'triple ARV')),
        blank=True,
        null=True)

    # TODO: skip_logic infant_prohylaxis: display field only if perinatally infected = YES
    infant_prohylaxis = models.CharField(
        max_length=25,
        verbose_name='Did the individual receive infant prophylaxis in the 1st month of life?',
        choices=YES_NO_UNKNOWN)

    # TODO: skip_logic infant_prohylaxis_rx: display field only if infant prophylaxis=YES
    infant_prohylaxis_rx = models.CharField(
        max_length=25,
        verbose_name='Please specify type of infant prophylaxis in the 1st month of life ',
        choices=(('sdnvp', 'sdNVP'), ('azt', 'AZT'), ('extended_nvp', 'Extended NVP')),
        blank=True,
        null=True)

    art_history = models.ManyToManyField(
        ARTRegimen,
        verbose_name='Prior History of ARV Treatments')

    counseling = models.CharField(
        max_length=25,
        verbose_name='Did this person receive adherence counseling?',
        choices=YES_NO_UNKNOWN)

    # TODO: skip_logic counseling_date: display field only if adherence counseling= YES
    counseling_date = models.DateField(
        verbose_name='Date of Adherence Counseling',
        blank=True,
        null=True)

    # TODO: skip_logic adherence_partner_rel: display field only if adherence counseling= YES
    adherence_partner_rel = models.CharField(
        max_length=25,
        verbose_name='Relationship of Adherence Partner to Individual',
        choices=(('mother', 'Mother'), ('father', 'Father'), ('grandmother', 'Grandmother'), ('grandfather', 'Grandfather'), ('aunt', 'Aunt'), ('uncle', 'Uncle'), ('partner_or_spouse', 'Partner or Spouse'), ('sister', 'Sister'), ('brother', 'Brother'), ('friend', 'Friend'), ('legal_guardian', 'Legal Guardian'), ('OTHER', 'Other (describe)'), ('unable_to_ascertain', 'Unable to Ascertain')),
        blank=True,
        null=True)

    # TODO: skip_logic adherence_partner_rel_other: display field only if relationship to adherence parter= OTHER
    adherence_partner_rel_other = models.CharField(
        max_length=25,
        verbose_name='Please describe  "Other" relationship',
        blank=True,
        null=True)

    class Meta:
        app_label = 'ba_namotswe'
