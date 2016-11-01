from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer, AdminDateWidget
from django.utils import timezone

from edc_constants.constants import ON_STUDY, YES, NO, UNKNOWN, NOT_APPLICABLE
from edc_visit_tracking.choices import VISIT_REASON, VISIT_INFO_SOURCE
from edc_visit_tracking.constants import SCHEDULED, CHART
from edc_visit_tracking.form_mixins import VisitFormMixin

from .choices import VISIT_STUDY_STATUS
from .models import (
    SubjectVisit, Oi, OiRecord, Enrollment, EntryToCare, Death, AdherenceCounselling,
    Tb, TbRecord, PregnancyHistory, Transfer, TransferRecord, ArtRecord, ArtRegimen, LabRecord, LabTest,
    WhoStaging, WhoDiagnosis, LostToFollowup)
from .validators import (
    SimpleYesNoValidationMixin, SimpleOtherSpecifyValidationMixin,
    SimpleDateFieldValidatorMixin, SimpleStartStopDateValidationMixin)
from ba_namotswe.validators import SimpleApplicableByAgeValidatorMixin


class SubjectVisitForm(VisitFormMixin, forms.ModelForm):

    participant_label = 'patient'

    visit_date = forms.DateField(
        label='Clinic visit date',
        initial=timezone.now,
        help_text="",
        widget=AdminDateWidget(),
    )

    report_datetime = forms.DateTimeField(
        label='Clinic visit date',
        initial=timezone.now,
        required=False,
        help_text="",
        widget=AdminDateWidget(),
    )

    study_status = forms.ChoiceField(
        label='Study status',
        choices=VISIT_STUDY_STATUS,
        initial=ON_STUDY,
        required=False,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer)
    )

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        initial=SCHEDULED,
        required=False,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        label='Source of information',
        initial='chart',
        required=False,
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    dashboard_type = 'subject'

    def clean(self):
        self.cleaned_data['study_status'] = ON_STUDY
        self.cleaned_data['reason'] = SCHEDULED
        self.cleaned_data['info_source'] = CHART
        cleaned_data = super(SubjectVisitForm, self).clean()
        try:
            obj = SubjectVisit.objects.filter(
                subject_identifier=cleaned_data['appointment'].subject_identifier,
                visit_date=cleaned_data['visit_date']).exclude(pk=self.instance.pk)
        except AttributeError:
            obj = SubjectVisit.objects.filter(
                subject_identifier=cleaned_data['appointment'].subject_identifier,
                visit_date=cleaned_data['visit_date'])
        if obj:
            raise forms.ValidationError({
                'visit_date': 'Visit already reported for {}'.format(
                    cleaned_data['visit_date'].strftime('%Y-%m-%d'))})
        try:
            previous_visit_code = cleaned_data['appointment'].schedule.get_previous_visit(
                cleaned_data['appointment'].visit_code).code
            try:
                obj = SubjectVisit.objects.get(
                    subject_identifier=cleaned_data['appointment'].subject_identifier,
                    visit_code=previous_visit_code)
                if obj.visit_date > cleaned_data['visit_date']:
                    raise forms.ValidationError({
                        'visit_date': 'Visit date must be after {}. See visit {}.'.format(
                            obj.visit_date.strftime('%Y-%m-%d'),
                            previous_visit_code)})
            except SubjectVisit.DoesNotExist:
                pass
        except AttributeError:
            pass
        return cleaned_data

    class Meta:
        model = SubjectVisit
        fields = ['appointment', 'visit_date']


class EnrollmentForm(SimpleOtherSpecifyValidationMixin, forms.ModelForm):

    def clean(self):
        self.require_if_other('caregiver_relation', 'caregiver_relation_other')
        return self.cleaned_data

    class Meta:
        model = Enrollment
        fields = '__all__'


class EntryToCareForm(SimpleYesNoValidationMixin, SimpleOtherSpecifyValidationMixin,
                      SimpleDateFieldValidatorMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(EntryToCareForm, self).clean()
        self.validate_date_with_dob('entry_date', 'gte', verbose_name='Entry date')
        self.validate_date_with_dob('hiv_dx_date', 'gte', verbose_name='HIV Dx date')
        self.validate_dates(
            'hiv_dx_date', 'lte', 'entry_date',
            verbose_name1='HIV Dx date', verbose_name2='Entry date')
        self.validate_dates(
            'art_init_date', 'gte', 'hiv_dx_date',
            verbose_name1='ART initiation date', verbose_name2='HIV Dx date')
        self.require_if_yes('weight_measured', 'weight')
        self.require_if_yes('height_measured', 'height')
        self.validate_perinatal_infection_arvs()
        self.require_if_other('art_preg_type', 'art_preg_type_other')
        return cleaned_data

    def validate_perinatal_infection_arvs(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('art_preg') == YES and cleaned_data.get('art_preg_type') == NOT_APPLICABLE:
            raise forms.ValidationError({
                'art_preg_type': ['Mother received ARVs during pregnancy, please complete.']})
        elif cleaned_data.get('art_preg') in [NO, UNKNOWN] and cleaned_data.get('art_preg_type') != NOT_APPLICABLE:
            raise forms.ValidationError({
                'art_preg_type': ['Mother did not received ARVs during pregnancy, please correct.']})

    class Meta:
        model = EntryToCare
        fields = '__all__'


class InCareForm(SimpleYesNoValidationMixin, SimpleOtherSpecifyValidationMixin,
                 SimpleDateFieldValidatorMixin, SimpleApplicableByAgeValidatorMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(InCareForm, self).clean()
        self.require_if_yes('weight_measured', 'weight')
        self.require_if_yes('height_measured', 'height')
        self.require_if_yes('hospital', 'hospital_date')
        self.require_if_yes('hospital', 'hospital_reason')
        self.require_if_yes('disclosure_to_patient', 'disclosure_to_patient_date')
        self.require_if_yes('disclosure_to_others', 'disclosure_to_others_date')
        self.validate_date_with_previous_visit(
            'hospital_date', 'gte', verbose_name='Hospital date')
        self.validate_date_with_previous_visit(
            'disclosure_to_patient_date', 'gte', verbose_name='Disclosure date')
        self.validate_date_with_previous_visit(
            'disclosure_to_others_date', 'gte', verbose_name='Disclosure date')
        self.validate_date_with_previous_visit(
            'disclosure_by_caregiver_date', 'gte', verbose_name='Disclosure date')
        self.validate_applicable_by_age('disclosure_by_caregiver', 'lte', 18)
        return cleaned_data


class AdherenceCounsellingForm(SimpleOtherSpecifyValidationMixin, SimpleDateFieldValidatorMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(AdherenceCounsellingForm, self).clean()
        self.validate_date_with_entry_to_care_date(
            'counselling_date', 'gte', verbose_name='Counselling date')
        self.validate_counselling_partner()
        return cleaned_data

    def validate_counselling_partner(self):
        return self.require_if_other('relation', 'relation_other')

    class Meta:
        model = AdherenceCounselling
        fields = '__all__'


class OiForm(SimpleStartStopDateValidationMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(OiForm, self).clean()
        if cleaned_data.get('oi'):
            self.validate_start_stop_dates()

    class Meta:
        model = Oi
        fields = '__all__'


class OiRecordForm (forms.ModelForm):

    class Meta:
        model = OiRecord
        fields = '__all__'


class ArtRegimenForm (SimpleStartStopDateValidationMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(ArtRegimenForm, self).clean()
        if cleaned_data.get('regimen'):
            self.validate_start_stop_dates()

    class Meta:
        model = ArtRegimen
        fields = '__all__'


class ArtRecordForm (forms.ModelForm):

    class Meta:
        model = ArtRecord
        fields = '__all__'


class DeathForm (forms.ModelForm):

    class Meta:
        model = Death
        fields = '__all__'


class LostToFollowupForm (forms.ModelForm):

    class Meta:
        model = LostToFollowup
        fields = '__all__'


class TbForm(SimpleOtherSpecifyValidationMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(TbForm, self).clean()
        self.require_if_other('dx_method', 'dx_method_other')
        return cleaned_data

    class Meta:
        model = Tb
        fields = '__all__'


class TBRecordForm(forms.ModelForm):

    class Meta:
        model = TbRecord
        fields = '__all__'


class PregnancyHistoryForm (forms.ModelForm):

    class Meta:
        model = PregnancyHistory
        fields = '__all__'


class TransferForm(SimpleOtherSpecifyValidationMixin, forms.ModelForm):

    def clean(self):
        self.require_if_other('transfer_to', 'transfer_to_other')
        self.require_if_other('transfer_from', 'transfer_from_other')

    class Meta:
        model = Transfer
        fields = '__all__'


class TransferRecordForm (forms.ModelForm):

    def clean(self):
        cleaned_data = super(TransferRecordForm, self).clean()
        self.validate_transferred()
        return cleaned_data

    def validate_transferred(self):
        for field in ['transferred_to', 'transferred_from']:
            if self.cleaned_data.get(field) and not self.cleaned_data.get('{}_other'.format(field)):
                raise forms.ValidationError({
                    '{}_other'.format(field): [
                        'Please specify where the patient was {}'.format(' '.join(field.split('_')))]})
            else:
                if self.cleaned_data.get('{}_other'.format(field)):
                    raise forms.ValidationError({
                        '{}_other'.format(field): [
                            'Location selected above. Please leave blank']})

    class Meta:
        model = TransferRecord
        fields = '__all__'


class LabTestForm(forms.ModelForm):

    class Meta:
        model = LabTest
        fields = ['utest_id', 'quantifier', 'value', 'test_date']

    def clean(self):
        super(LabTestForm, self).clean()
        if not self.cleaned_data['test_date']:
            self.cleaned_data['test_date'] = self.cleaned_data['lab_record'].subject_visit.visit_date
        print(self.cleaned_data)
        if self.cleaned_data.get('value') and self.cleaned_data.get('utest_id'):
            self.validate_value()
        return self.cleaned_data

    def validate_value(self):
        if self.cleaned_data['utest_id'] == 'CD4':
            if int(self.cleaned_data['value']) < 0 or int(self.cleaned_data['value']) > 2000:
                raise forms.ValidationError({'value': 'Invalid value'})
        if self.cleaned_data['utest_id'] == 'CD4_perc':
            if int(self.cleaned_data['value']) < 0 or int(self.cleaned_data['value']) > 100:
                raise forms.ValidationError({'value': 'Invalid value'})
        if self.cleaned_data['utest_id'] == 'VL':
            if int(self.cleaned_data['value']) < 40 or int(self.cleaned_data['value']) > 750000:
                raise forms.ValidationError({'value': 'Invalid value'})


class LabRecordForm(forms.ModelForm):

    class Meta:
        model = LabRecord
        fields = '__all__'


class WhoDiagnosisForm(SimpleDateFieldValidatorMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(WhoDiagnosisForm, self).clean()
        subject_identifier = cleaned_data.get('who_staging').subject_identifier
        self.validate_date_with_dob(
            'dx_date', 'gte', verbose_name='Dx date', subject_identifier=subject_identifier)
        self.validate_date_with_hiv_dx(
            'dx_date', 'gte', verbose_name='Dx date', subject_identifier=subject_identifier)
        self.validate_date_with_art_init(
            'dx_date', 'lte', verbose_name='Dx date', subject_identifier=subject_identifier)
        return cleaned_data

    class Meta:
        model = WhoDiagnosis
        fields = '__all__'


class WhoStagingForm(forms.ModelForm):

    class Meta:
        model = WhoStaging
        fields = '__all__'
