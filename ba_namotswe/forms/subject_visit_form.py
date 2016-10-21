from django import forms

from edc_visit_tracking.form_mixins import VisitFormMixin
from ba_namotswe.models import SubjectVisit
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer
from edc_visit_tracking.choices import VISIT_REASON, VISIT_INFO_SOURCE
from edc_constants.constants import ON_STUDY


class SubjectVisitForm(VisitFormMixin, forms.ModelForm):

    study_status = forms.ChoiceField(
        label='What is the mother\'s current study status',
        choices=VISIT_REASON,
        initial=ON_STUDY,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer)
    )

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        label='Source of information',
        required=False,
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    dashboard_type = 'subject'

    class Meta:
        model = SubjectVisit
        fields = '__all__'
