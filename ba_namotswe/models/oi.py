from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel


class Oi(BaseUuidModel):

    CANDIDIASIS_OF_BRONCHI = 'CANDIDIASIS_OF_BRONCHI_TRACHEA_ESOPHAGUS_OR_LUNGS'
    INVASIVE_CERVICAL_CANCER = 'INVASIVE_CERVICAL_CANCER'
    COCCIDIOIDOMYCOSIS = 'COCCIDIOIDOMYCOSIS'
    CRYPTOCOCCOSIS = 'CRYPTOCOCCOSIS'
    CRYPTOSPORIDIOSIS = 'CRYPTOSPORIDIOSIS_CHRONIC_INTESTINAL_GREATER_THAN_1_MONTH_DURATION'
    CTYTOMEGALOVIRUS = 'CTYTOMEGALOVIRUS_DISEASE'
    ENCEPHALOPHALOPATHY = 'ENCEPHALOPHALOPAHY_HIV_RELATED'
    HERPES_SIMPLEX = 'HERPES_SIMPLEX'
    HISTOPLASMOSIS = 'HISTOPLASMOSIS'
    ISOSPORIASIS = 'ISOSPORIASIS_CHRONIC_INTESTINAL_GREATER_THAN_1_MONTH_DURATION'
    KAPOSI_SARCOMA = 'KAPOSI_SARCOMA'
    LYMPHOMA = 'LYMPHOMA'
    MYCOBACTERIUM_AVIUM_COMPLEX = 'MYCOBACTERIUM_AVIUM_COMPLEX'
    TUBERCULOSIS = 'TUBERCULOSIS'
    PNEUMOCYSTIS = 'PNEUMOCYSTIS_JIROVECI_PNEUMONIA'
    PNEUMONIA = 'PNEUMONIA_RECURRENT'
    PROGRESSIVE_MULTILOCAL_LEUKOENCEPHALOPATHY = 'PROGRESSIVE_MULTILOCAL_LEUKOENCEPHALOPATHY'
    SALMONELLA_SEPTICEMIA_RECURRENT = 'SALMONELLA_SEPTICEMIA_RECURRENT'
    TOXOPLASMOSIS_OF_BRAIN = 'TOXOPLASMOSIS_OF_BRAIN'
    WASTING_SYNDROME_DUE_TO_HIV = 'WASTING_SYNDROME_DUE_TO_HIV'
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

    oi_type = models.CharField(
        max_length=10,
        choices=OI_OPTIONS)

    def __str__(self):
        return self.display_name

    class Meta:
        app_label = 'ba_namotswe'
