from django import forms

from ba_namotswe.models import Abstraction


class AbstractionForm (forms.ModelForm):

    class Meta:
        model = Abstraction
        fields = '__all__'
