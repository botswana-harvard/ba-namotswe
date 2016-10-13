from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from edc_visit_tracking.model_mixins import CrfModelMixin

from .subject_visit import SubjectVisit


class AssessmentHistory(CrfModelMixin, UpdatesCrfMetadataModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    cd4_count = models.IntegerField(
        verbose_name='CD4+ Cell Count',
        blank=True,
        null=True)

    cd4_perc = models.IntegerField(
        verbose_name='CD4+ %',
        blank=True,
        null=True)

    # TODO: skip_logic vl_count: display field only if Date of Initial Visit < May 1st, 2008
    vl_count = models.CharField(
        max_length=25,
        verbose_name='Viral Load',
        validators=[],  # TODO: accept =/>/< and integer)
        blank=True,
        null=True)

    alt = models.IntegerField(
        verbose_name='ALT(SGPT)',
        blank=True,
        null=True)

    hgb = models.IntegerField(
        verbose_name='Hgb',
        blank=True,
        null=True)

    ldl = models.IntegerField(
        verbose_name='LDL',
        blank=True,
        null=True)

    syphillis = models.IntegerField(
        verbose_name='Syphillis',
        blank=True,
        null=True)

    test_other = models.IntegerField(
        verbose_name='Other (add option to "click to add more fields)',
        blank=True,
        null=True)

    class Meta:
        app_label = 'ba_namotswe'
