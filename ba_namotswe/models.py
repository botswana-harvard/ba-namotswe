from django.db import models
from django.utils import timezone

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_base.model.validators.date import date_not_future
from edc_constants.choices import GENDER, YES_NO, YES_NO_UNKNOWN
from edc_metadata.model_mixins import CreatesMetadataModelMixin, UpdatesCrfMetadataModelMixin
from edc_registration.model_mixins import RegisteredSubjectModelMixin, RegisteredSubjectMixin
from edc_visit_tracking.model_mixins import VisitModelMixin, PreviousVisitModelMixin, CrfModelMixin
from edc_appointment.model_mixins import AppointmentModelMixin


class RegisteredSubject(RegisteredSubjectModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'ba_namotswe'


class Enrollment(BaseUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject)

    report_datetime = models.DateTimeField(default=timezone.now)

    is_eligible = models.BooleanField(default=True)

    dob = models.DateField(
        verbose_name='Date of Birth',
        validators=[date_not_future, ])

    gender = models.CharField(
        max_length=25,
        verbose_name='Gender',
        choices=GENDER)

    initial_visit_date = models.DateField(
        verbose_name='Date of Initial Clinic Visit',
        validators=[date_not_future, ])

    # TODO: skip_logic caregiver_relation: display field only if 10 years ago _ DOB _ 13 years ago? (adolescents only--ASK AT SLH)
    caregiver_relation = models.CharField(
        verbose_name='Caregiver/Next of Kin Relationship',
        max_length=25,
        choices=(
            ('mother', 'Mother'),
            ('father', 'Father'),
            ('grandmother', 'Grandmother'),
            ('grandfather', 'Grandfather'),
            ('aunt', 'Aunt'),
            ('uncle', 'Uncle'),
            ('legal_guardian', 'Legal Guardian'),
            ('OTHER', 'Other (describe))')),
        help_text='Please describe the caregiver/next of kin\'s relationship to patient')

    # TODO: skip_logic caregiver_relation_other: display field only if Caregiver/Next of Kin Relationship= OTHER
    caregiver_relation_other = models.CharField(
        max_length=25,
        verbose_name='Caregiver/Next of Kin Relationship: "Other"',
        blank=True,
        null=True)

    weight_measured = models.CharField(
        max_length=25,
        verbose_name='Weight was measured at Initial Clinic Visit',
        choices=YES_NO)

    weight = models.IntegerField(
        verbose_name='Weight',
        blank=True,
        null=True)

    height_measured = models.CharField(
        max_length=25,
        verbose_name='Height was measured at Initial Clinic Visit',
        choices=YES_NO)

    height = models.IntegerField(
        verbose_name='Height was measured at Initial Clinic Visit',
        blank=True,
        null=True)

    hiv_diagnosis_date = models.DateField(
        verbose_name='HIV Diagnosis Date ',
        validators=[date_not_future, ],
        blank=True,
        null=True,
        help_text='Leave blank if diagnosis date is same as initial visit date')

    art_initiation_date = models.DateField(
        verbose_name='ART Initiation Date',
        validators=[date_not_future, ])

    def save(self, *args, **kwargs):
        if not self.hiv_diagnosis_date:
            self.hiv_diagnosis_date = self.initial_visit_date
        super(Enrollment, self).save(*args, **kwargs)

    class Meta:
        app_label = 'ba_namotswe'


class Appointment(AppointmentModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'ba_namotswe'


class SubjectVisit(VisitModelMixin, CreatesMetadataModelMixin, PreviousVisitModelMixin, BaseUuidModel):

    enrollment = models.ForeignKey(Enrollment)

    appointment = models.OneToOneField(Appointment)

    class Meta:
        app_label = 'ba_namotswe'


class ARTRegimen(BaseUuidModel):

    name = models.CharField(max_length=10)

    display_name = models.CharField(max_length=25)

    def __str__(self):
        return self.display_name

    class Meta:
        app_label = 'ba_namotswe'


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


class Io(BaseUuidModel):

    name = models.CharField(max_length=10)

    display_name = models.CharField(max_length=25)

    def __str__(self):
        return self.display_name

    class Meta:
        app_label = 'ba_namotswe'


class Abstraction(CrfModelMixin, UpdatesCrfMetadataModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    height_measured = models.CharField(
        max_length=25,
        verbose_name='Was height measured at this clinic visit?',
        choices=YES_NO)

    # TODO: skip_logic height: display field only if patient if patient is under the age of 19 OR if they are an adult  and do not have a previous height recorded. (adults only need one height for the study)
    height = models.IntegerField(
        verbose_name='Height at Current Clinic Visit',
        blank=True,
        null=True)

    weight_measured = models.CharField(
        max_length=25,
        verbose_name='Was weight measured at this clinic visit?',
        choices=YES_NO)

    # TODO: skip_logic weight: display field only if patient is under the age of 19 OR if they are an adult  and do not have a previous height recorded. (adults only need one height for the study)
    weight = models.IntegerField(
        verbose_name='Weight at Current Clinic Visit',
        blank=True,
        null=True)

    hospitalized = models.CharField(
        max_length=25,
        verbose_name='Has the patient been hospitalized since last visit?',
        choices=YES_NO_UNKNOWN)

    # TODO: skip_logic hospitalized_date: display field only if hospitalization=YES
    hospitalized_date = models.DateField(
        verbose_name='What was the date of the hospitalization?',
        blank=True,
        null=True)

    # TODO: skip_logic hospitalized_reason: display field only  if hospitalization=YES
    hospitalized_reason = models.CharField(
        max_length=25,
        verbose_name='What was the reason for the hospitalization?',
        blank=True,
        null=True)

    art_history = models.ManyToManyField(
        ARTRegimen,
        verbose_name='ARV regimens',
        help_text='Please select all ART regimens since last visit')

    tb = models.CharField(
        max_length=25,
        verbose_name='Has the patient been diagnosed with TB since the last visit?',
        choices=YES_NO)

    # TODO: skip_logic tb_type: display field only if TB since last visit=YES
    tb_type = models.CharField(
        max_length=25,
        verbose_name='Type of TB',
        choices=(('pulmonary_tb', 'Pulmonary TB'), ('non-pulmonary_tb', 'Non-pulmonary TB')),
        blank=True,
        null=True)

    # TODO: skip_logic tb_method: display field only if TB since last visit=YES
    tb_method = models.CharField(
        max_length=25,
        verbose_name='Method of TB diagnosis',
        choices=(('culture_positive', 'Culture Positive'), ('cxr', 'CXR'), ('other_imaging_modality', 'Other Imaging Modality'), ('clinical_diagnosis', 'Clinical Diagnosis'), ('other_(describe)', 'Other (describe)')),
        blank=True,
        null=True)

    # TODO: skip_logic tb_method_other: display field only if Method of TB Diagnosis= OTHER
    tb_method_other = models.CharField(
        max_length=25,
        verbose_name='Method of TB diagnosis: Other',
        blank=True,
        null=True)

    io = models.CharField(
        max_length=25,
        verbose_name='Non-TB Opportunistic Infections since last visit',
        choices=YES_NO)

    # TODO: skip_logic io_history_table: display field only if non-TB OI since last visit=YES
    io_history = models.ManyToManyField(
        Io,
        verbose_name='Opportunistic Infections Since last visit')

    ctx = models.CharField(
        max_length=25,
        verbose_name='Has this patient used Cotrimoxazole /Dapsone Prophylaxis since last visit?',
        choices=YES_NO)

    # TODO: skip_logic ctx_table: display field only if Clotrimoxazole/Dapsone Prophylaxis=YES
    ctx_table = models.CharField(
        max_length=25,
        verbose_name='Did the patient receive Cotrimoxazole or Dapsone prophylaxis',
        choices=(('cotrimoxazole', 'Cotrimoxazole'), ('dapsone', 'Dapsone')),
        blank=True,
        null=True)

    # TODO: skip_logic pregnant_and_rx: display field only  if sex= FEMALE
    pregnant_and_rx = models.CharField(
        max_length=25,
        verbose_name='Has this patient been pregnant while on treatment?',
        choices=YES_NO)

    # TODO: skip_logic pregnant_and_rx_table: display field only if pregnancy= YES
    pregnant_and_rx_table = models.CharField(
        max_length=25,
        verbose_name='Details of pregnancies while on treatment')

    # TODO: skip_logic hiv_status_aware: display field only if age _19(ASK LIZ)
    hiv_status_aware = models.CharField(
        max_length=25,
        verbose_name='Is there evidence that disclosure has been made to the youth/adolescent that they are HIV-infected?',
        choices=YES_NO_UNKNOWN)

    # TODO: skip_logic hiv_status_aware_date: show if disclosure=YES
    hiv_status_aware_date = models.DateField(
        verbose_name='Date of disclosure',
        blank=True,
        null=True)

    hiv_disclosed_others = models.CharField(
        max_length=25,
        verbose_name='Is there evidence that the individual has disclosed their HIV status to others?',
        choices=YES_NO_UNKNOWN,
        blank=True,
        null=True)

    # TODO: skip_logic hiv_caregiver_disclosed_others: display field only if age _19(ASK LIZ)
    hiv_caregiver_disclosed_others = models.CharField(
        max_length=25,
        verbose_name='For youth and adolescents, is there evidence that the caregiver has disclosed their HIV status to others?',
        choices=YES_NO_UNKNOWN)

    transferred = models.CharField(
        max_length=25,
        verbose_name='Transfer of Care',
        choices=YES_NO)

    # TODO: skip_logic transferred_table: show if transfer of care=YES
    transferred_table = models.CharField(
        max_length=25,
        verbose_name='Transfer of Care Details')

    # TODO: skip_logic transferred_to: show if transfer of care=YES
    transferred_to = models.CharField(
        max_length=25,
        verbose_name='Location of transfer',
        choices=(('into_idcc', 'Into IDCC'), ('out_of_idcc', 'Out of IDCC'), ('into_private_clinic', 'Into Private Clinic'), ('out_of_private_clinic', 'Out of Private Clinic'), ('into_bipai', 'Into BIPAI'), ('out_of_bipai', 'Out of BIPAI'), ('other_(describe)', 'Other (Describe)')),
        blank=True,
        null=True)

    # TODO: skip_logic transferred_to_other: show if location of transfer= OTHER
    transferred_to_other = models.CharField(
        max_length=25,
        verbose_name='Location of transfer: Other',
        blank=True,
        null=True)

    deceased = models.CharField(
        max_length=25,
        verbose_name='Is there documentation of mortality on the patient\'s chart?',
        choices=YES_NO)

    # TODO: skip_logic death_date: show if mortality=YES
    death_date = models.DateField(
        verbose_name='Date of Death',
        validators=[date_not_future, ],
        blank=True,
        null=True)

    # TODO: skip_logic death_cause: display field only if mortality=YES
    death_cause = models.CharField(
        max_length=25,
        verbose_name='Cause of Death',
        blank=True,
        null=True)

    class Meta:
        app_label = 'ba_namotswe'


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
