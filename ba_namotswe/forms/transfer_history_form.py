from django import forms

from ba_namotswe.models.transfer_history import TransferHistory


class TransferHistoryForm (forms.ModelForm):

    class Meta:
        model = TransferHistory

    def clean(self):
        if self.cleaned_data['transfer_loc']:
            self.validate_other_tb_diagnosis()
        return self.cleaned_data

    def validate_other_transfer_loc(self):
        if self.cleaned_data['transfer_loc']:
            if not self.cleaned_data['transfer_loc_other']:
                raise forms.ValidationError({
                    'transfer_loc_other': [
                        'You have to enter other transfer_loc as you have selected other in Transfer location']})
        else:
            if self.cleaned_data['transfer_loc_other']:
                raise forms.ValidationError({
                    'transfer_loc_other': [
                        'You should not enter other transfer_location as you have already selected a transfer_location']})