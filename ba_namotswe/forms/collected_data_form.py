from django import forms

from ba_namotswe.models import CollectedData


class CollectedDataForm (forms.ModelForm):

    class Meta:
        model = CollectedData
        fields = '__all__'
