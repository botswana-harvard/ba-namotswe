from django import forms

from ba_namotswe.models import Oi


class OiForm (forms.ModelForm):

    class Meta:
        model = Oi
        fields = '__all__'
