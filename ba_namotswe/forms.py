from datetime import date, timedelta

from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer, AdminDateWidget
from django.utils import timezone

from edc_base.utils.age import age
from edc_constants.constants import ON_STUDY, OTHER, YES, NO, UNKNOWN, NOT_APPLICABLE
from edc_visit_tracking.choices import VISIT_REASON, VISIT_INFO_SOURCE
from edc_visit_tracking.constants import SCHEDULED
from edc_visit_tracking.form_mixins import VisitFormMixin

from .models import (
    SubjectVisit, Oi, OiRecord, Enrollment, EntryToCare, Death, AdherenceCounselling, ExtractionChecklist,
    Tb, TbRecord, PregnancyHistory, TransferRecord, ArtRecord, ArtRegimen, LabRecord, WhoStaging)
from .choices import VISIT_STUDY_STATUS
from .constants import ONGOING
from ba_namotswe.models.transfer_record import Transfer


class SimpleYesNoValidationMixin:

    def require_if_yes(self, yesno_field, required_field, required_msg=None, not_required_msg=None):
        if self.cleaned_data.get(yesno_field) in [NO, UNKNOWN] and self.cleaned_data.get(required_field):
            raise forms.ValidationError({
                required_field: [not_required_msg or 'Field is not required based on answer above']})
        elif self.cleaned_data.get(yesno_field) == YES and not self.cleaned_data.get(required_field):
            raise forms.ValidationError({
                required_field: [required_msg or 'Field is required based on answer of YES above']})


class SimpleOtherSpecifyValidationMixin:

    def require_if_other(self, other_field, specify_field, required_msg=None, not_required_msg=None):
        if self.cleaned_data.get(other_field) != OTHER and self.cleaned_data.get(specify_field):
            raise forms.ValidationError({
                specify_field: [not_required_msg or 'Field is not required']})
        elif self.cleaned_data.get(other_field) == OTHER and not self.cleaned_data.get(specify_field):
            raise forms.ValidationError({
                specify_field: [required_msg or 'Specify answer for OTHER']})


class SimpleStartStopDateValidationMixin:
    def validate_start_stop_dates(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get('started'):
            raise forms.ValidationError({'started': 'Required'})
        if cleaned_data.get('status') != ONGOING and not cleaned_data.get('stopped'):
            raise forms.ValidationError({'stopped': 'Required'})
        if cleaned_data.get('status') == ONGOING and cleaned_data.get('stopped'):
            raise forms.ValidationError({'stopped': 'Expected blank'})
        if cleaned_data.get('started') - cleaned_data.get('stopped') == timedelta(days=0):
            raise forms.ValidationError({'stopped': 'Cannot be equal'})
        if cleaned_data.get('started') - cleaned_data.get('stopped') > timedelta(days=0):
            raise forms.ValidationError({'stopped': 'Cannot be less than started'})


class SubjectVisitForm(VisitFormMixin, forms.ModelForm):

    report_datetime = forms.DateTimeField(
        label='Report date',
        initial=timezone.now,
        help_text="",
        widget=AdminDateWidget(),
    )

    study_status = forms.ChoiceField(
        label='Study status',
        choices=VISIT_STUDY_STATUS,
        initial=ON_STUDY,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer)
    )

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        initial=SCHEDULED,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        label='Source of information',
        initial='chart',
        required=False,
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    dashboard_type = 'subject'

    class Meta:
        model = SubjectVisit
        fields = ['appointment', 'report_datetime', 'study_status', 'reason', 'info_source']


class EnrollmentForm(forms.ModelForm):

    def clean(self):
        self.validate_initial_visit_date()
        self.validate_caregiver_relation_age()
        self.validate_caregiver_relation_other()
        self.validate_hiv_diagnosis_date()
        self.validate_hiv_art_initiation()
        return self.cleaned_data

    def validate_initial_visit_date(self):
        start_date = date(2002, 1, 1)
        end_date = date(2016, 6, 1)
        if self.cleaned_data.get('initial_visit_date'):
            if self.cleaned_data.get('initial_visit_date') < start_date:
                raise forms.ValidationError({
                    'initial_visit_date': [
                        'Initial visit date should come after January 1st, 2002']})
            elif self.cleaned_data.get('initial_visit_date') > end_date:
                raise forms.ValidationError({
                    'initial_visit_date': [
                        'Initial visit date should come before June 1st, 2016']})

    def validate_caregiver_relation_age(self):
        registered_subject = self.cleaned_data.get('registered_subject')
        if registered_subject:
            if self.cleaned_data.get('initial_visit_date'):
                age_at_visit = age(registered_subject.dob, self.cleaned_data.get('initial_visit_date')).years
                if (age_at_visit >= 10) & (age_at_visit <= 13):
                    if not self.cleaned_data.get('caregiver_relation'):
                        raise forms.ValidationError({
                            'caregiver_relation': [
                                'Subject was between 10 and 13, you have to provide']})
                    elif self.cleaned_data.get('caregiver_relation') == 'not_applicable':
                        raise forms.ValidationError({
                            'caregiver_relation': [
                                'Subject was between 10 and 13 years of age, you have to provide caregiver']})

    def validate_caregiver_relation_other(self):
        if self.cleaned_data.get('caregiver_relation') != OTHER:
            if self.cleaned_data.get('caregiver_relation_other'):
                raise forms.ValidationError({
                    'caregiver_relation_other': [
                        'You should not enter other caregiver relation as you have already entered a caregiver relation']})
        else:
            if not self.cleaned_data.get('caregiver_relation_other'):
                raise forms.ValidationError({
                    'caregiver_relation_other': [
                        'You should enter other caregiver relation as you have selected OTHER caregiver relation']})

    def validate_hiv_diagnosis_date(self):
        if self.cleaned_data.get('registered_subject'):
            if self.cleaned_data.get('hiv_diagnosis_date'):
                if self.cleaned_data.get('hiv_diagnosis_date') < self.cleaned_data.get('registered_subject').dob:
                    raise forms.ValidationError({
                        'hiv_diagnosis_date': [
                            'Diagnosis date should come after date of birth']})

    def validate_hiv_art_initiation(self):
        if self.cleaned_data.get('art_initiation_date'):
            if self.cleaned_data.get('hiv_diagnosis_date'):
                if self.cleaned_data.get('art_initiation_date') < self.cleaned_data.get('hiv_diagnosis_date'):
                    raise forms.ValidationError({
                        'art_initiation_date': [
                            'ART Initiation date should come after diagnosis date']})

    class Meta:
        model = Enrollment
        fields = '__all__'


class EntryToCareForm(SimpleYesNoValidationMixin, SimpleOtherSpecifyValidationMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(EntryToCareForm, self).clean()
        self.validate_weight()
        self.validate_height()
        self.validate_perinatal_infection_arvs()
        self.validate_art_preg_type()
        return cleaned_data

    def validate_perinatal_infection_arvs(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('art_preg') == YES and cleaned_data.get('art_preg_type') == NOT_APPLICABLE:
            raise forms.ValidationError({
                'art_preg_type': ['Mother received ARVs during pregnancy, please complete.']})
        elif cleaned_data.get('art_preg') in [NO, UNKNOWN] and cleaned_data.get('art_preg_type') != NOT_APPLICABLE:
            raise forms.ValidationError({
                'art_preg_type': ['Mother did not received ARVs during pregnancy, please correct.']})

    def validate_art_preg_type(self):
        return self.require_if_other('art_preg_type', 'art_preg_type_other')

    def validate_weight(self):
        return self.require_if_yes('weight_measured', 'entry_weight')

    def validate_height(self):
        return self.require_if_yes('height_measured', 'entry_height')

    class Meta:
        model = EntryToCare
        fields = '__all__'


class ExtractionChecklistForm (forms.ModelForm):

    class Meta:
        model = ExtractionChecklist
        fields = '__all__'


class AdherenceCounsellingForm(SimpleOtherSpecifyValidationMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super(AdherenceCounsellingForm, self).clean()
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


class LabRecordForm(forms.ModelForm):

    class Meta:
        model = LabRecord
        fields = '__all__'


class WhoStagingForm(forms.ModelForm):

    class Meta:
        model = WhoStaging
        fields = '__all__'
