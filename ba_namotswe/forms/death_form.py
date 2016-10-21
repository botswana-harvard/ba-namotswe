from django import forms

from ba_namotswe.models.death import Death


class DeathForm (forms.ModelForm):

    class Meta:
        model = Death
        fields = '__all__'
