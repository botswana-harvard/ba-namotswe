from django import forms

from ba_namotswe.models import Extraction


class ExtractionForm (forms.ModelForm):

    class Meta:
        model = Extraction
        fields = '__all__'
