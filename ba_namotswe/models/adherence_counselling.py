from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel


class Adherence_Counselling(BaseUuidModel):

    class Meta:
        app_label = 'ba_namotswe'

    adherence_date = models.DateField(
        verbose_name='Date of Adherence Counseling',
        blank=True,
        null=True)

    adherence_partner = models.CharField(
        verbose_name='Relationship of Adherence Partner to Individual',
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
            ('sister', 'Sister'),
            ('legal_guardian', 'Legal Guardian'),
            ('not_applicable', 'Not Applicable'),
            ('OTHER', 'Other, specify')),

    adherence_partner_other = models.CharField(
        max_length=25,
        verbose_name='adherence partner: "Other"',
        blank=True,
        null=True)