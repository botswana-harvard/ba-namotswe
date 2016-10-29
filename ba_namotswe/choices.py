from edc_constants.constants import UNKNOWN, OTHER, ON_STUDY, OFF_STUDY, NOT_APPLICABLE

from .constants import (
    CANDIDIASIS_OF_BRONCHI, INVASIVE_CERVICAL_CANCER, COCCIDIOIDOMYCOSIS, CRYPTOCOCCOSIS,
    CRYPTOSPORIDIOSIS, ENCEPHALOPHALOPATHY, HERPES_SIMPLEX, HISTOPLASMOSIS,
    ISOSPORIASIS, KAPOSI_SARCOMA, LYMPHOMA, MYCOBACTERIUM_AVIUM_COMPLEX, TUBERCULOSIS, PNEUMOCYSTIS,
    PNEUMONIA, PROGRESSIVE_MULTILOCAL_LEUKOENCEPHALOPATHY, SALMONELLA_SEPTICEMIA_RECURRENT,
    TOXOPLASMOSIS_OF_BRAIN, WASTING_SYNDROME_DUE_TO_HIV, PULMONARY_TB, NON_PULMONARY_TB,
    CULTURE_POSITIVE, CXR, OTHER_IMAGING_MODALITY, CLINICAL_DIAGNOSIS, ONGOING, RESOLVED, RESOLVED_EST)


ART_STATUS = (
    (ONGOING, 'Ongoing'),
    ('HELD', 'Held'),
    ('STOPPED', 'Stopped'),
    ('INITIAL', 'Initial'),
)

OI_STATUS = (
    (ONGOING, 'Ongoing'),
    (RESOLVED, 'Resolved'),
    (RESOLVED_EST, 'Resolved/Estimated'),
)

# ART_REGIMENS = (
#     ('EFV/TDF/FTC', 'NNRTI: EFV + TDF/FTC'),
#     ('EFV + ABC/3TC', 'NNRTI: EFV + ABC/3TC'),
#     ('RPV/TDF/FTC', 'NNRTI: RPV + TDF/FTC)'),
#     ('(DRV/r) + TDF/FTC', 'PI: Darunavir/ritonavir (DRV/r) + TDF/FTC'),
#     ('ATV/r + ABC/3TC', 'PI: ATV/r + ABC/3TC'),
#     ('DRV/r + ABC/3TC', 'PI: DRV/r + ABC/3TC'),
#     ('LPV/r + ABC/3TC', 'PI: Lopinavir/ritonavir LPV/r + ABC/3TC'),
#     ('LPV/r + ABC/3TC', 'PI: Lopinavir/ritonavir LPV/r + TDF/FTC'),
#     ('(RAL) + TDF/FTC', 'INSTI: Raltegravir (RAL) + TDF/FTC'),
#     ('RAL + ABC/3TC', 'INSTI: Raltegravir (RAL) + ABC/3TC'),
#     ('EVG/COBI/TDF/FTC', 'INSTI: EVG/COBI/TDF/FTC'),
#     ('(DTG) + ABC/3TC', 'INSTI: Dolutegravir (DTG) + ABC/3TC'),
#     ('DTG + TDF/FTC', 'INSTI: Dolutegravir (DTG) + + TDF/FTC'),
# )

ART_REGIMENS = (
    ('EFV+FTC+TDF', 'Atripla (FTC, TDF, EFV)'),
    ('3TC+AZT', 'Combivir (AZT, 3TC)'),
    ('3TC+ABC+AZT', 'Trizivir (AZT, 3TC, ABC)'),
    ('FTC+TDF', 'Truvada (TDF, FTC)'),
    ('3TC', '3TC'),
    ('ABC', 'Abacavir/ABC'),
    ('AZT', 'ATZ'),
    ('D4T', 'D4T'),
    ('DDI', 'DDI'),
    ('DTG', 'Dolutegravir/DTG'),
    ('EFV', 'Efavirenz/EFV (or Sustiva)'),
    ('FTC', 'Emtricitabine/FTC (Emtriva)'),
    ('IDV', 'Indinavir/IDV'),
    ('KTA', 'Kaletra/KTA (or Alulia)'),
    ('NFV', 'Nelfinavir/NFV'),
    ('NVP', 'Nevirapine/NVP'),
    ('RAL', 'Raltegravir/RAL'),
    ('TDF', 'Tenofovir/TDF'),
    (UNKNOWN, 'Unknown'),
    (OTHER, 'Other, specify...'),
)

VISIT_STUDY_STATUS = (
    (ON_STUDY, 'On Study'),
    (OFF_STUDY, 'Off Study'),
)

UTEST_IDS = (
    ('CD4', 'CD4 absolute'),
    ('CD4_perc', 'CD4 percentage'),
    ('VL', 'Viral Load'),
)

MATERNAL_ARVS = (
    ('AZT', 'AZT Monotherapy'),
    ('sdNVP', 'Single-dose NVP'),
    ('AZT-sdNVP', 'AZT and dsNVP'),
    ('tripleARV', 'triple ARV'),
    (OTHER, 'Other, please specify'),
    (NOT_APPLICABLE, 'Not applicable'),

)

QUANTIFIERS = (
    ('<', '<'),
    ('<=', '<='),
    ('=', '= '),
    ('>=', '>='),
    ('>', '>'),
)

INFANT_PROPHYLAXIS = (
    ('sdNVP', 'Single-dose NVP'),
    ('AZT', 'AZT Monotherapy'),
    ('AZT-sdNVP', 'AZT and dsNVP'),
    ('extNVP', 'Extended NVP'),
    (NOT_APPLICABLE, 'Not applicable'),
)

WHO_STAGE = (
    ('I', 'Stage I'),
    ('II', 'Stage II'),
    ('III', 'Stage III'),
    ('IV', 'Stage IV'),
    (UNKNOWN, 'Unknown'),
)

WHO_DEFINING_ILLNESSES = (
    ('A1', 'Asymptomatic'),
    ('A2', 'Persistent generalized lymphadenopathy (PGL)'),

    ('B040', 'Angular cheilitis'),
    ('B080', 'Fungal nail infections of fingers'),
    ('B030', 'Herpes zoster'),
    ('B050', 'Oral ulcerations, recurrent'),
    ('B060', 'Papular pruritic eruptions'),
    ('B020', 'Respiratory tract infections, recurrent (RTIs, sinusitis, bronchitis, otitis media, pharyngitis)'),
    ('B070', 'Seborrhoeic dermatitis'),
    ('B010', 'Weigh loss, moderate unexplained (<10% of presumed or measured body weight)'),
    ('B011', 'Weight loss, severe (>10% of presumed or measured body weight)'),

    ('C090', 'Acute necrotizing ulcerative stomatitis, gingivitis or periodontitis'),
    ('C100', 'Anaemia, unexplained (<8 g/dl), and or neutropenia (<500/mm3) and or'),
    ('C070', 'Bacterial infections, severe presumed  (e.g. pneumonia, empyema, pyomyositis, bone or'),
    ('C020', 'Chronic diarrhoea, unexplained, (for longer than one month)'),
    ('C080', 'Joint infection, meningitis, bacteraemia'),
    ('C040', 'Oral candidiasis'),
    ('C050', 'Oral hairy leukoplakia'),
    ('C030', 'Persistent fever, unexplained (intermittent or constant for longer than one month)'),
    ('C060', 'Pulmonary tuberculosis (TB) diagnosed in last two years'),
    ('C110', 'Thrombocytopenia (<50 000/ mm3) for more than one month'),

    ('D080', 'Central nervous system (CNS) toxoplasmosis'),
    ('D040', 'Chronic herpes simplex infection (orolabial, genital or anorectal of more than one month’s duration)'),
    ('D060', 'Extrapulmonary TB'),
    ('D090', 'HIV encephalopathy'),
    ('D010', 'HIV wasting syndrome'),
    ('D070', 'Kaposi’s sarcoma'),
    ('D050', 'Oesophageal candidiasis'),
    ('D020', 'Pneumocystis pneumonia'),
    ('D030', 'Recurrent severe or radiological bacterial pneumonia'),

    # Conditions where confirmatory diagnostic testing is necessary
    ('E190', 'Any disseminated mycosis (e.g. histoplasmosis, coccidiomycosis, penicilliosis)'),
    ('E140', 'Candida of trachea, bronchi or lungs'),
    ('E150', 'Cryptosporidiosis'),
    ('E180', 'Cytomegalovirus (CMV) infection (retinitis or of an organ other than liver, spleen or lymph nodes)'),
    ('E120', 'Disseminated non-tuberculous mycobacteria infection'),
    ('E110', 'Extrapulmonary cryptococcosis including meningitis'),
    ('E220', 'Invasive cervical carcinoma'),
    ('E160', 'Isosporiasis'),
    ('E210', 'Lymphoma (cerebral or B cell non-Hodgkin)'),
    ('E130', 'Progressive multifocal leukoencephalopathy (PML)'),
    ('E200', 'Recurrent non-typhoidal salmonella septicaemia'),
    ('E170', 'Visceral herpes simplex infection'),
    ('E230', 'Visceral leishmaniasis'),
)


TB_TYPE = (
    (PULMONARY_TB, 'Pulmonary TB'),
    (NON_PULMONARY_TB, 'Non pulmonary TB'),
    (UNKNOWN, 'Unknown'),
)

TEST_TYPE = (
    (CULTURE_POSITIVE, 'Culture Positive'),
    (CXR, 'CXR'),
    (OTHER_IMAGING_MODALITY, 'Other Imaging Modality'),
    (CLINICAL_DIAGNOSIS, 'Clinical Diagnosis'),
    (OTHER, 'Other, describe'),
    (UNKNOWN, 'Unknown'),
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

TRANSFER = (
    ('idcc', 'IDCC'),
    ('private', 'Private Clinic'),
    ('bipai', 'BIPAI'),
    (OTHER, 'Other, specify'))

RELATIONSHIP = (
    ('mother', 'Mother'),
    ('father', 'Father'),
    ('grandmother', 'Grandmother'),
    ('grandfather', 'Grandfather'),
    ('aunt', 'Aunt'),
    ('uncle', 'Uncle'),
    ('sister', 'Sister'),
    ('legal_guardian', 'Legal Guardian'),
    (NOT_APPLICABLE, 'Not Applicable'),
    (OTHER, 'Other, specify'),
    (UNKNOWN, 'Unknown'),
)
