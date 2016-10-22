from django import forms

from ba_namotswe.models import ArtRegimen


class ArtRegimenForm (forms.ModelForm):

    class Meta:
        model = ArtRegimen
        fields = '__all__'
