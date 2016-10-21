from django import forms

from edc_consent.form_mixins import ConsentFormMixin

from ..models import DummyConsent


class DummyConsentForm(ConsentFormMixin, forms.ModelForm):

    class Meta:
        model = DummyConsent
        fields = '__all__'
