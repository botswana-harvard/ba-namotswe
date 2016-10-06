from django import forms
from datetime import date
from edc_constants.constants import NOT_APPLICABLE, MALE, FEMALE
from ..choices import RELATIONS, FEMALE_RELATIONS, MALE_RELATIONS

from ba_namotswe.models import RegisteredSubject

class RegisteredSubjectForm(forms.ModelForm):

    def clean(self):
        self.validate_dob()
        return self.cleaned_data

    def validate_dob(self):
        if age(self.cleaned_data['dob'], date.today()).years < 10:
            raise forms.ValidationError({
                'dob': [
                    'Date of birth should be at least 10 years ago']})
            
    def validate_on_gender(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('gender') == MALE:
            if cleaned_data.get('relation') not in [item[0] for item in RELATIONS if item not in FEMALE_RELATIONS]:
                raise forms.ValidationError(
                    'Member is Male but you selected a female relation. Got {0}.'.format(
                        [item[1] for item in RELATIONS if item[0] == cleaned_data.get('relation')][0]))
        if cleaned_data.get('gender') == FEMALE:
            if cleaned_data.get('relation') not in [item[0] for item in RELATIONS if item not in MALE_RELATIONS]:
                raise forms.ValidationError(
                    'Member is Female but you selected a male relation. Got {0}.'.format(
                        [item[1] for item in RELATIONS if item[0] == cleaned_data.get('relation')][0]))

    class Meta:
        model = RegisteredSubject
        fields = '__all__'
