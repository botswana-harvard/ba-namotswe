# from django.db import models
# 
# from edc_base.model.validators.date import date_not_future
# from edc_constants.choices import YES_NO, YES_NO_UNKNOWN
# 
# from .art_regimen import ArtRegimen
# from .crf_model import CrfModel
# from .oi import Oi
# 
# 
# class Extraction(CrfModel):
# 
#     height_measured = models.CharField(
#         max_length=25,
#         verbose_name='Was height measured at this clinic visit?',
#         choices=YES_NO)
# 
#     # TODO: skip_logic height: display field only if patient if patient is under the age of 19 OR if they are an adult  and do not have a previous height recorded. (adults only need one height for the study)
#     height = models.IntegerField(
#         verbose_name='Height at Current Clinic Visit',
#         blank=True,
#         null=True)
# 
#     weight_measured = models.CharField(
#         max_length=25,
#         verbose_name='Was weight measured at this clinic visit?',
#         choices=YES_NO)
# 
#     # TODO: skip_logic weight: display field only if patient is under the age of 19 OR if they are an adult  and do not have a previous height recorded. (adults only need one height for the study)
#     weight = models.IntegerField(
#         verbose_name='Weight at Current Clinic Visit',
#         blank=True,
#         null=True)
# 
#     hospitalized = models.CharField(
#         max_length=25,
#         verbose_name='Has the patient been hospitalized since last visit?',
#         choices=YES_NO_UNKNOWN)
# 
#     # TODO: skip_logic hospitalized_date: display field only if hospitalization=YES
#     hospitalized_date = models.DateField(
#         verbose_name='What was the date of the hospitalization?',
#         blank=True,
#         null=True)
# 
#     # TODO: skip_logic hospitalized_reason: display field only  if hospitalization=YES
#     hospitalized_reason = models.CharField(
#         max_length=25,
#         verbose_name='What was the reason for the hospitalization?',
#         blank=True,
#         null=True)
# 
#     art_history = models.ManyToManyField(
#         ArtRegimen,
#         verbose_name='ARV regimens',
#         help_text='Please select all ART regimens since last visit')
# 
#     tb = models.CharField(
#         max_length=25,
#         verbose_name='Has the patient been diagnosed with TB since the last visit?',
#         choices=YES_NO)
# 
#     # TODO: skip_logic tb_type: display field only if TB since last visit=YES
#     tb_type = models.CharField(
#         max_length=25,
#         verbose_name='Type of TB',
#         choices=(('pulmonary_tb', 'Pulmonary TB'), ('non-pulmonary_tb', 'Non-pulmonary TB')),
#         blank=True,
#         null=True)
# 
#     # TODO: skip_logic tb_method: display field only if TB since last visit=YES
#     tb_method = models.CharField(
#         max_length=25,
#         verbose_name='Method of TB diagnosis',
#         choices=(('culture_positive', 'Culture Positive'), ('cxr', 'CXR'), ('other_imaging_modality', 'Other Imaging Modality'), ('clinical_diagnosis', 'Clinical Diagnosis'), ('other_(describe)', 'Other (describe)')),
#         blank=True,
#         null=True)
# 
#     # TODO: skip_logic tb_method_other: display field only if Method of TB Diagnosis= OTHER
#     tb_method_other = models.CharField(
#         max_length=25,
#         verbose_name='Method of TB diagnosis: Other',
#         blank=True,
#         null=True)
# 
#     io = models.CharField(
#         max_length=25,
#         verbose_name='Non-TB Opportunistic Infections since last visit',
#         choices=YES_NO)
# 
#     # TODO: skip_logic io_history_table: display field only if non-TB OI since last visit=YES
#     io_history = models.ManyToManyField(
#         Oi,
#         verbose_name='Opportunistic Infections Since last visit')
# 
#     ctx = models.CharField(
#         max_length=25,
#         verbose_name='Has this patient used Cotrimoxazole /Dapsone Prophylaxis since last visit?',
#         choices=YES_NO)
# 
#     # TODO: skip_logic ctx_table: display field only if Clotrimoxazole/Dapsone Prophylaxis=YES
#     ctx_table = models.CharField(
#         max_length=25,
#         verbose_name='Did the patient receive Cotrimoxazole or Dapsone prophylaxis',
#         choices=(('cotrimoxazole', 'Cotrimoxazole'), ('dapsone', 'Dapsone')),
#         blank=True,
#         null=True)
# 
#     # TODO: skip_logic pregnant_and_rx: display field only  if sex= FEMALE
#     pregnant_and_rx = models.CharField(
#         max_length=25,
#         verbose_name='Has this patient been pregnant while on treatment?',
#         choices=YES_NO)
# 
#     # TODO: skip_logic pregnant_and_rx_table: display field only if pregnancy= YES
#     pregnant_and_rx_table = models.CharField(
#         max_length=25,
#         verbose_name='Details of pregnancies while on treatment')
# 
#     # TODO: skip_logic hiv_status_aware: display field only if age _19(ASK LIZ)
#     hiv_status_aware = models.CharField(
#         max_length=25,
#         verbose_name='Is there evidence that disclosure has been made to the youth/adolescent that they are HIV-infected?',
#         choices=YES_NO_UNKNOWN)
# 
#     # TODO: skip_logic hiv_status_aware_date: show if disclosure=YES
#     hiv_status_aware_date = models.DateField(
#         verbose_name='Date of disclosure',
#         blank=True,
#         null=True)
# 
#     hiv_disclosed_others = models.CharField(
#         max_length=25,
#         verbose_name='Is there evidence that the individual has disclosed their HIV status to others?',
#         choices=YES_NO_UNKNOWN,
#         blank=True,
#         null=True)
# 
#     # TODO: skip_logic hiv_caregiver_disclosed_others: display field only if age _19(ASK LIZ)
#     hiv_caregiver_disclosed_others = models.CharField(
#         max_length=25,
#         verbose_name='For youth and adolescents, is there evidence that the caregiver has disclosed their HIV status to others?',
#         choices=YES_NO_UNKNOWN)
# 
#     transferred = models.CharField(
#         max_length=25,
#         verbose_name='Transfer of Care',
#         choices=YES_NO)
# 
#     # TODO: skip_logic transferred_table: show if transfer of care=YES
#     transferred_table = models.CharField(
#         max_length=25,
#         verbose_name='Transfer of Care Details')
# 
#     # TODO: skip_logic transferred_to: show if transfer of care=YES
#     transferred_to = models.CharField(
#         max_length=25,
#         verbose_name='Location of transfer',
#         choices=(('into_idcc', 'Into IDCC'), ('out_of_idcc', 'Out of IDCC'), ('into_private_clinic', 'Into Private Clinic'), ('out_of_private_clinic', 'Out of Private Clinic'), ('into_bipai', 'Into BIPAI'), ('out_of_bipai', 'Out of BIPAI'), ('other_(describe)', 'Other (Describe)')),
#         blank=True,
#         null=True)
# 
#     # TODO: skip_logic transferred_to_other: show if location of transfer= OTHER
#     transferred_to_other = models.CharField(
#         max_length=25,
#         verbose_name='Location of transfer: Other',
#         blank=True,
#         null=True)
# 
#     deceased = models.CharField(
#         max_length=25,
#         verbose_name='Is there documentation of mortality on the patient\'s chart?',
#         choices=YES_NO)
# 
#     # TODO: skip_logic death_date: show if mortality=YES
#     death_date = models.DateField(
#         verbose_name='Date of Death',
#         validators=[date_not_future, ],
#         blank=True,
#         null=True)
# 
#     # TODO: skip_logic death_cause: display field only if mortality=YES
#     death_cause = models.CharField(
#         max_length=25,
#         verbose_name='Cause of Death',
#         blank=True,
#         null=True)
# 
#     class Meta(CrfModel.Meta):
#         app_label = 'ba_namotswe'
