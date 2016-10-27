from datetime import date

from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_base.utils.age import age
from edc_constants.constants import ON_STUDY, OTHER, YES, NO
from edc_visit_tracking.choices import VISIT_REASON, VISIT_INFO_SOURCE
from edc_visit_tracking.form_mixins import VisitFormMixin

from .models import (
    SubjectVisit, OiRecord, Enrollment, EntryToCare, Death, AdherenceCounselling, ExtractionChecklist,
    TbRecord, PregnancyHistory, TransferRecord, ArtRecord, LabRecord, WhoStaging)


class SubjectVisitForm(VisitFormMixin, forms.ModelForm):

    study_status = forms.ChoiceField(
        label='What is the mother\'s current study status',
        choices=VISIT_REASON,
        initial=ON_STUDY,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer)
    )

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        label='Source of information',
        required=False,
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    dashboard_type = 'subject'

    class Meta:
        model = SubjectVisit
        fields = '__all__'


class EnrollmentForm(forms.ModelForm):

    def clean(self):
        self.validate_initial_visit_date()
        self.validate_caregiver_relation_age()
        self.validate_caregiver_relation_other()
        self.validate_weight()
        self.validate_height()
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

    def validate_weight(self):
        if self.cleaned_data.get('weight_measured') == NO:
            if self.cleaned_data.get('weight'):
                raise forms.ValidationError({
                    'weight': [
                        'You should not enter weight']})
        elif self.cleaned_data.get('weight_measured') == YES:
            if not self.cleaned_data.get('weight'):
                raise forms.ValidationError({
                    'weight': [
                        'You should enter the weight']})
            self.ensure_right_weight()

    def ensure_right_weight(self):
        if self.cleaned_data.get('weight') > 136:
                raise forms.ValidationError({
                    'weight': [
                        'Weight should be less than 136 kilos']})
        elif self.cleaned_data.get('weight') < 20:
                raise forms.ValidationError({
                    'weight': [
                        'Weight should be greater than 20 kilos']})

    def validate_height(self):
        if self.cleaned_data.get('height_measured') == NO:
            if self.cleaned_data.get('height'):
                raise forms.ValidationError({
                    'height': [
                        'You should not enter height']})
        elif self.cleaned_data.get('height_measured') == YES:
            if not self.cleaned_data.get('height'):
                raise forms.ValidationError({
                    'height': [
                        'You should enter the height']})
            self.ensure_right_height()

    def ensure_right_height(self):
        if self.cleaned_data.get('height') > 244:
                raise forms.ValidationError({
                    'height': [
                        'Height should be less than 244cm']})
        elif self.cleaned_data.get('height') < 100:
                raise forms.ValidationError({
                    'height': [
                        'Height should be greater than 100cm']})

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
        if self.cleaned_data.get('caregiver_relation') != 'OTHER':
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


class EntryToCareForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(EntryToCareForm, self).clean()
        self.validate_perinatal_infection_pmtct()
        return cleaned_data

    def validate_perinatal_infection_pmtct(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('phiv') == YES and not self.cleaned_data.get('art_preg'):
            raise forms.ValidationError({
                'art_preg': ['Infant was perinatally infected, please complete.']})
        return cleaned_data

    def validate_perinatal_infection_pmtct_rx(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('art_preg') == YES and not cleaned_data.get('art_preg_type'):
            raise forms.ValidationError({
                'art_preg_type': ['Mother received ARVs during pregnancy, please complete.']})
        return cleaned_data

    class Meta:
        model = EntryToCare
        fields = '__all__'


class ExtractionChecklistForm (forms.ModelForm):

    class Meta:
        model = ExtractionChecklist
        fields = '__all__'


class AdherenceCounsellingForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(AdherenceCounsellingForm, self).clean()
        self.validate_adherence_partne_relation_other()
        return cleaned_data

    def validate_adherence_partner_relation_other(self):
        if self.cleaned_data.get('adherence_partner_relation') != OTHER:
            if self.cleaned_data.get('adherence_partner_relation_other'):
                raise forms.ValidationError({
                    'adherence_partne_relation_other': [
                        'You should not enter other adherence_partner relation as you have already entered a adherence_partner relation']})
        else:
            if not self.cleaned_data.get('adherence_partner_relation_other'):
                raise forms.ValidationError({
                    'adherence_partner_relation_other': [
                        'You should enter other adherence_partner relation as you have selected OTHER adherence_partner relation']})
        return self.cleaned_data

    class Meta:
        model = AdherenceCounselling
        fields = '__all__'


class OiRecordForm (forms.ModelForm):

    class Meta:
        model = OiRecord
        fields = '__all__'


class ArtRecordForm (forms.ModelForm):

    class Meta:
        model = ArtRecord
        fields = '__all__'


class DeathForm (forms.ModelForm):

    class Meta:
        model = Death
        fields = '__all__'


class TBRecordForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(TBRecordForm, self).clean()
        self.validate_dx_method()
        return cleaned_data

    def validate_dx_method(self):
        if self.cleaned_data.get('dx_method') == OTHER and not self.cleaned_data.get('dx_method_other'):
                raise forms.ValidationError({
                    'dx_method_other': [
                        'Option OTHER was selected above, please specify...']})
        else:
            if self.cleaned_data.get('dx_method_other'):
                raise forms.ValidationError({
                    'dx_method_other': [
                        'A TB test has been specified above. Expect blank.']})

    class Meta:
        model = TbRecord
        fields = '__all__'


class PregnancyHistoryForm (forms.ModelForm):

    class Meta:
        model = PregnancyHistory
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
