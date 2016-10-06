from django import forms
from ba_namotswe.models import SubjectVisit, RegisteredSubject


class SubjectVisitForm(forms.ModelForm):

    def clean(self):
        self.validate_report_datetime()

    def validate_report_datetime(self):
        enrol = self.cleaned_data.get('enrollment')
        registered_subject = enrol.registered_subject
        dob = registered_subject.dob
        if self.cleaned_data.get('appointment'):
            if self.cleaned_data.get("report_datetime") < dob:
                raise forms.ValidationError("Report datetime cannot be before consent datetime")
            if self.cleaned_data.get("report_datetime").date() < dob:
                raise forms.ValidationError("Report datetime cannot be before DOB")

    class Meta:
        model = SubjectVisit
        fields = '__all__'
