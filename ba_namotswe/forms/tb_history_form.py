from django import forms
from ba_namotswe.models.tb_history import TBHistory, OTHER


class TBHistoryForm(forms.ModelForm):

    def clean(self):
        if self.cleaned_data['tb_test']:
            self.validate_other_tb_diagnosis()
        return self.cleaned_data

    def validate_other_tb_diagnosis(self):
        if self.cleaned_data['tb_test'] == OTHER:
            if not self.cleaned_data['tb_test_other']:
                raise forms.ValidationError({
                    'tb_test_other': [
                        'You have to enter other TB test as you have selected other in TB Test']})
        else:
            if self.cleaned_data['tb_test_other']:
                raise forms.ValidationError({
                    'tb_test_other': [
                        'You should not enter other TB test as you have already selected a TB Test']})

    class Meta:
        model = TBHistory
        fields = '__all__'
