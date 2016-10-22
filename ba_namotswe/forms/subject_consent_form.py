from django import forms

from edc_consent.form_mixins import ConsentFormMixin

from ba_namotswe.models import SubjectConsent


class SubjectConsentForm(ConsentFormMixin, forms.ModelForm):

    class Meta:
        model = SubjectConsent
        fields = '__all__'
