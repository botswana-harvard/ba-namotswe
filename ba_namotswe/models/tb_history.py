from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_base.model.validators.date import date_not_future

PULMONARY_TB = 'PULMONARY TB'
NON_PULMONARY_TB = 'NON PULMONARY TB'
CULTURE_POSITIVE = 'CULTURE POSITIVE'
CXR = 'CXR'
OTHER_IMAGING_MODALITY = 'OTHER IMAGING MODALITY'
CLINICAL_DIAGNOSIS = 'CLINICAL DIAGNOSIS'
OTHER = 'OTHER'

TB_TYPE = (
    (PULMONARY_TB, 'Pulmonary TB'),
    (NON_PULMONARY_TB, 'Non pulmonary TB'),
)

TEST_TYPE = (
    (CULTURE_POSITIVE, 'Culture Positive'),
    (CXR, 'CXR'),
    (OTHER_IMAGING_MODALITY, 'Other Imaging Modality'),
    (CLINICAL_DIAGNOSIS, 'Clinical Diagnosis'),
    (OTHER, 'Other, describe')
)


class TBHistory(BaseUuidModel):

    tb_date = models.DateField(
        verbose_name='Date of TB diagnosis',
        validators=[date_not_future, ])

    tb_type = models.CharField(
        verbose_name='Type of TB',
        max_length=30,
        choices=TB_TYPE)

    tb_test = models.CharField(
        verbose_name='Method of TB diagnosis',
        max_length=30,
        choices=TEST_TYPE)

    tb_test_other = models.CharField(
        verbose_name='Method of TB diagnosis: Other',
        blank=True,
        null=True,
        max_length=50)
