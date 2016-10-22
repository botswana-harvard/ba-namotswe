from .contants import (CANDIDIASIS_OF_BRONCHI, INVASIVE_CERVICAL_CANCER, COCCIDIOIDOMYCOSIS, CRYPTOCOCCOSIS,
                       CRYPTOSPORIDIOSIS, ENCEPHALOPHALOPATHY, HERPES_SIMPLEX, HISTOPLASMOSIS,
                       ISOSPORIASIS, KAPOSI_SARCOMA, LYMPHOMA, MYCOBACTERIUM_AVIUM_COMPLEX, TUBERCULOSIS, PNEUMOCYSTIS,
                       PNEUMONIA, PROGRESSIVE_MULTILOCAL_LEUKOENCEPHALOPATHY, SALMONELLA_SEPTICEMIA_RECURRENT,
                       TOXOPLASMOSIS_OF_BRAIN, WASTING_SYNDROME_DUE_TO_HIV, PULMONARY_TB, NON_PULMONARY_TB,
                       CULTURE_POSITIVE, CXR, OTHER_IMAGING_MODALITY, CLINICAL_DIAGNOSIS, OTHER, UNCERTAIN)
from edc_constants.constants import YES, NO

YES_NO_UNCERTAIN = (
    (YES, 'Yes'),
    (NO, 'No'),
    (UNCERTAIN, 'Unable to ascertain'),
)


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

OI_OPTIONS = (
    (CANDIDIASIS_OF_BRONCHI, 'Candidiasis of bronchi, trachea, esophagus, or lungs'),
    (INVASIVE_CERVICAL_CANCER, 'Invasive cervical cancer'),
    (COCCIDIOIDOMYCOSIS, 'Coccidioidomycosis'),
    (CRYPTOCOCCOSIS, 'Cryptococcosis'),
    (CRYPTOSPORIDIOSIS, 'Cryptosporidiosis, chronic intestinal (greater than 1 months duration)'),
    (ENCEPHALOPHALOPATHY, 'Encephalopathy, HIV-related'),
    (HERPES_SIMPLEX, 'Herpes simplex: chronic ulcer(s) (greater than 1 month duration); or bronchitis, pneumonitis, or esophagitis'),
    (HISTOPLASMOSIS, 'Histoplasmosis'),
    (ISOSPORIASIS, 'Isosporiasis, chronic intestinal (greater than 1 months duration)'),
    (KAPOSI_SARCOMA, "Kaposi's sarcoma"),
    (LYMPHOMA, 'Lymphoma, multiple forms'),
    (MYCOBACTERIUM_AVIUM_COMPLEX, 'Mycobacterium avium complex'),
    (TUBERCULOSIS, 'Tuberculosis'),
    (PNEUMOCYSTIS, 'Pneumocystis jiroveci pneumonia (PJP)'),
    (PNEUMONIA, 'Pneumonia, recurrent'),
    (PROGRESSIVE_MULTILOCAL_LEUKOENCEPHALOPATHY, 'Progressive multifocal leukoencephalopathy'),
    (SALMONELLA_SEPTICEMIA_RECURRENT, 'Salmonella septicemia, recurrent'),
    (TOXOPLASMOSIS_OF_BRAIN, 'Toxoplasmosis of brain'),
    (WASTING_SYNDROME_DUE_TO_HIV, 'Wasting syndrome due to HIV')
)

PREGNANCY = (
    ('date_of_first_clinical_documentation_of_pregnancy', 'Date of First Clinical Documentation of Pregnancy'),
    ('date_of_delivery', 'Date of Delivery'))

TRANSFER = (
    ('into_idcc', 'Into IDCC'),
    ('out_of_idcc', 'Out of IDCC'),
    ('into private_clinic', 'Into Private Clinic'),
    ('out_of_private_clinic', 'Out of Private Clinic'),
    ('into_bipai', 'Into BIPAI'),
    ('out_of_bipai', 'Out of BIPAI'),
    ('OTHER', 'Other, specify'))

RELATIONSHIP = (
    ('mother', 'Mother'),
    ('father', 'Father'),
    ('grandmother', 'Grandmother'),
    ('grandfather', 'Grandfather'),
    ('aunt', 'Aunt'),
    ('uncle', 'Uncle'),
    ('sister', 'Sister'),
    ('legal_guardian', 'Legal Guardian'),
    ('not_applicable', 'Not Applicable'),
    ('OTHER', 'Other, specify'))
