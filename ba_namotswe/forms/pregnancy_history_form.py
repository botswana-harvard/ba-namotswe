from django import forms

from ba_namotswe.models.pregnancy_history import PregnancyHistory


class PregnancyHistoryForm (forms.ModelForm):

    class Meta:
        model = PregnancyHistory
