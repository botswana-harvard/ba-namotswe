from django import forms

from ba_namotswe.models import AssessmentHistory


class AssessmentHistoryForm (forms.ModelForm):

    class Meta:
        model = AssessmentHistory
        fields = '__all__'
