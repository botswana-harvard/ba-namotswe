from django import forms

from ba_namotswe.models import PregnancyHistory


class PregnancyHistoryForm (forms.ModelForm):

    class Meta:
        model = PregnancyHistory
        fields = '__all__'
