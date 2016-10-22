from django import forms

from ba_namotswe.models import ArvHistory


class ArvHistoryForm (forms.ModelForm):

    class Meta:
        model = ArvHistory
        fields = '__all__'
