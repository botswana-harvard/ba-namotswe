from django import forms

from ba_namotswe.models import RegisteredSubject
from edc_base.utils.age import age
from edc_constants.constants import NO, YES
from datetime import date


class RegisteredSubjectForm(forms.ModelForm):

    def clean(self):
        self.validate_dob()
        return self.cleaned_data

    def validate_dob(self):
        if age(self.cleaned_data['dob'], date.today()).years < 10:
            raise forms.ValidationError({
                'dob': [
                    'Date of birth should be at least 10 years ago']})

    class Meta:
        model = RegisteredSubject
        fields = '__all__'
