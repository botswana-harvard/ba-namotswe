from django import forms

from ba_namotswe.models import Treatment
from edc_constants.constants import YES


class TreatmentForm(forms.ModelForm):

    def clean(self):
        self.validate_perinatal_infection_pmtct()
        return self.cleaned_data

    def validate_perinatal_infection_pmtct(self):
        if self.cleaned_data.get('perinatal_infection'):
            if self.cleaned_data.get('perinatal_infection') == YES:
                if not self.cleaned_data.get('pmtct'):
                    raise forms.ValidationError({
                        'pmtct': [
                            'Cannot leave this question blank']})
            return self.cleaned_data

    def validate_perinatal_infection_pmtct_rx(self):
        if self.cleaned_data.get('perinatal_infection'):
            if self.cleaned_data.get('perinatal_infection') == YES:
                if not self.cleaned_data.get('pmtct'):
                    raise forms.ValidationError({
                        'pmtct_rx': [
                            'Cannot leave this question blank']})
            return self.cleaned_data

    class Meta:
        model = Treatment
        fields = '__all__'
