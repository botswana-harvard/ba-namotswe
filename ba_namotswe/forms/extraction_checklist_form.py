from django import forms

from ba_namotswe.models import ExtractionChecklist


class ExtractionChecklistForm (forms.ModelForm):

    class Meta:
        model = ExtractionChecklist
        fields = '__all__'
