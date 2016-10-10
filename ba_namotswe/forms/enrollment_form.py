from django import forms

from edc_constants.constants import NOT_APPLICABLE

from ..models import Enrollment


class EnrollmentForm(forms.BaseModelForm):

    def validate_participant_enrollment(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('enrolled') == 'No':
            if not cleaned_data.get('confirm_enrollment') == NOT_APPLICABLE:
                raise forms.ValidationError('Confirmation of enrollment is not required.')

        if cleaned_data.get('enrolled') == 'Yes':
            if cleaned_data.get('confirm_enrollment') == NOT_APPLICABLE:
                raise forms.ValidationError('Confirmation of enrollment is required.')

    def validate_participant(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('record_number') == 'No':
            raise forms.ValidationError('Participant did not produced a medical record number, is a not yet enrolled')
        if cleaned_data.get('record_number') == 'yes':
            raise forms.ValidationError('Participant produced a medical record number, is enrolled ')

    def validate_date_of_birth(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('date_of_birth'):
            raise forms.ValidationError('participant date_of_birth is given .')
        if not cleaned_data.get('date_of_birth'):
            raise forms.ValidationError('participant weight is not given.')

    def validate_caregiver_relation_other(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('caregiver_relation_other') == 'Yes':
            raise forms.ValidationError('caregiver relation is other.')
        if cleaned_data.get('caregiver_relation_other') == False:
            raise forms.ValidationError('caregiver is next of kin.')

        if cleaned_data.get('next_of_kin') == False:
            raise forms.ValidationError('caregiver is not next of kin.')
        if cleaned_data.get('next_of_kin') == True:
            raise forms.ValidationError('caregiver is next of kin.')

        if cleaned_data.get('weight'):
            raise forms.ValidationError('participant weight is given .')
        if not cleaned_data.get('weight'):
            raise forms.ValidationError('participant weight is not given.')

        if cleaned_data.get('height'):
            raise forms.ValidationError('participant height is given .')
        if not cleaned_data.get('height'):
            raise forms.ValidationError('participant height is not given.')

        if cleaned_data.get('ART'):
            raise forms.ValidationError('participant given ART .')
        if not cleaned_data.get('ART'):
            raise forms.ValidationError('participant not given ART.')

    class Meta:
        model = Enrollment
