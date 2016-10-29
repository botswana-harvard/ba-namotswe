from datetime import timedelta
from django import forms
from edc_constants.constants import YES, NO, UNKNOWN, OTHER, NOT_APPLICABLE

from .constants import ONGOING
from .models import Enrollment, EntryToCare
from ba_namotswe.models.subject_visit import SubjectVisit
from dateutil.relativedelta import relativedelta

comparison_phrase = {
    'gt': 'must be greater than',
    'gte': 'must be greater than or equal to',
    'lt': 'must be less than',
    'lte': 'must be less than or equal to',
    'ne': 'may not equal', }


class SimpleApplicableByAgeValidatorMixin:
    def validate_applicable_by_age(self, field, op, age, subject_identifier=None, errmsg=None):
        subject_identifier = subject_identifier or self.cleaned_data.get('subject_visit').subject_identifier
        dob = Enrollment.objects.get(subject_identifier=subject_identifier).dob
        age_delta = relativedelta(self.cleaned_data.get('subject_visit').previous_visit().visit_date, dob)
        applicable = True
        if self.cleaned_data.get(field):
            applicable = False
            if op == 'gt':
                if age_delta.years > age:
                    applicable = True
            elif op == 'gte':
                if age_delta.years >= age:
                    applicable = True
            elif op == 'lt':
                if age_delta.years < age:
                    applicable = True
            elif op == 'lte':
                if age_delta.years <= age:
                    applicable = True
            elif op == 'ne':
                if age_delta.years != age:
                    applicable = True
            elif op == 'eq':
                if age_delta.years == age:
                    applicable = True
        if not applicable and self.cleaned_data.get(field) != NOT_APPLICABLE:
                raise forms.ValidationError({
                    field: [errmsg or ('Not applicable. Age {phrase} {age}y at previous visit. '
                                       'Got {subject_age}y').format(
                        phrase=comparison_phrase.get(op),
                        age=age, subject_age=age_delta.years)]})
        if applicable and self.cleaned_data.get(field) == NOT_APPLICABLE:
                raise forms.ValidationError({
                    field: [errmsg or ('Applicable. Age {phrase} {age}y at previous visit to be "not applicable". '
                                       'Got {subject_age}y').format(
                        phrase=comparison_phrase.get(op),
                        age=age, subject_age=age_delta.years)]})


class SimpleYesNoValidationMixin:

    def require_if_yes(self, yesno_field, required_field, required_msg=None, not_required_msg=None):
        if self.cleaned_data.get(yesno_field) in [NO, UNKNOWN] and self.cleaned_data.get(required_field):
            raise forms.ValidationError({
                required_field: [not_required_msg or 'This field is not required based on previous answer.']})
        elif self.cleaned_data.get(yesno_field) == YES and not self.cleaned_data.get(required_field):
            raise forms.ValidationError({
                required_field: [required_msg or 'This field is required based on previous answer.']})


class SimpleOtherSpecifyValidationMixin:

    def require_if_other(self, other_field, specify_field, required_msg=None, not_required_msg=None):
        if self.cleaned_data.get(other_field) != OTHER and self.cleaned_data.get(specify_field):
            raise forms.ValidationError({
                specify_field: [not_required_msg or 'This field is not required.']})
        elif self.cleaned_data.get(other_field) == OTHER and not self.cleaned_data.get(specify_field):
            raise forms.ValidationError({
                specify_field: [required_msg or 'Specify answer for OTHER.']})


class SimpleStartStopDateValidationMixin:
    def validate_start_stop_dates(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get('started'):
            raise forms.ValidationError({'started': 'Required.'})
        if cleaned_data.get('status') != ONGOING and not cleaned_data.get('stopped'):
            raise forms.ValidationError({'stopped': 'Required.'})
        if cleaned_data.get('status') == ONGOING and cleaned_data.get('stopped'):
            raise forms.ValidationError({'stopped': 'Leave blank.'})
        if cleaned_data.get('started') - cleaned_data.get('stopped') == timedelta(days=0):
            raise forms.ValidationError({'stopped': 'Cannot be equal.'})
        if cleaned_data.get('started') - cleaned_data.get('stopped') > timedelta(days=0):
            raise forms.ValidationError({'stopped': 'Cannot be less than started.'})


class SimpleDateFieldValidatorMixin:

    def validate_date_with_dob(self, field1, op, verbose_name=None, subject_identifier=None):
        """Validate that date is greater than subject's DoB."""
        subject_identifier = subject_identifier or self.cleaned_data.get('subject_visit').subject_identifier
        value2 = Enrollment.objects.get(subject_identifier=subject_identifier).dob
        self.validate_dates(field1, op, value2=value2, verbose_name1=verbose_name, verbose_name2='DoB')

    def validate_date_with_art_init(self, field1, op, verbose_name=None, subject_identifier=None):
        """Validate that date is greater than subject's ART initiation date."""
        subject_identifier = subject_identifier or self.cleaned_data.get('subject_visit').subject_identifier
        value2 = EntryToCare.objects.get(
            subject_visit__subject_identifier=subject_identifier).art_init_date
        self.validate_dates(field1, op, value2=value2, verbose_name1=verbose_name, verbose_name2='ART initiation date')

    def validate_date_with_hiv_dx(self, field1, op, verbose_name=None, subject_identifier=None):
        """Validate that date is greater than subject's HIV Dx date."""
        subject_identifier = subject_identifier or self.cleaned_data.get('subject_visit').subject_identifier
        value2 = EntryToCare.objects.get(
            subject_visit__subject_identifier=subject_identifier).hiv_dx_date
        self.validate_dates(field1, op, value2=value2, verbose_name1=verbose_name, verbose_name2='HIV Dx date')

    def validate_date_with_entry_to_care_date(self, field1, op, verbose_name=None, subject_identifier=None):
        """Validate that date is greater than subject's Entry-to-care date."""
        subject_identifier = subject_identifier or self.cleaned_data.get('subject_visit').subject_identifier
        value2 = EntryToCare.objects.get(
            subject_visit__subject_identifier=subject_identifier).entry_date
        self.validate_dates(field1, op, value2=value2, verbose_name1=verbose_name, verbose_name2='Entry-to-care date')

    def validate_date_with_previous_visit(self, field1, op, verbose_name=None, subject_identifier=None):
        """Validate that date is greater than subject's previous visit date."""
        subject_identifier = subject_identifier or self.cleaned_data.get('subject_visit').subject_identifier
        previous_visit = self.cleaned_data.get('subject_visit').previous_visit()
        self.validate_dates(field1, op, value2=previous_visit.visit_date,
                            verbose_name1=verbose_name,
                            verbose_name2='previous visit {} on {}'.format(
                                previous_visit.visit_code,
                                previous_visit.visit_date.strftime('%Y-%m-%d')))

    def validate_dates(self, field1=None, op=None, field2=None, errmsg=None,
                       verbose_name1=None, verbose_name2=None, value1=None, value2=None):
        """Validate that date1 is greater than date2."""
        date1 = self.cleaned_data.get(field1, value1)
        date2 = self.cleaned_data.get(field2, value2)
        if not self.compare_dates(date1, op, date2):
            raise forms.ValidationError({
                field1: [errmsg or '{field1} {phrase} {field2}.'.format(
                    field1=verbose_name1 or field1 or date1,
                    phrase=comparison_phrase.get(op),
                    field2=verbose_name2 or field2 or date2)]})

    def compare_dates(self, date1, op, date2):
        ret = True
        if date1 and date2:
            ret = False
            if op == 'gt':
                if date1 > date2:
                    ret = True
            elif op == 'gte':
                if date1 >= date2:
                    ret = True
            elif op == 'lt':
                if date1 < date2:
                    ret = True
            elif op == 'lte':
                if date1 <= date2:
                    ret = True
            elif op == 'ne':
                if date1 != date2:
                    ret = True
            elif op == 'eq':
                if date1 == date2:
                    ret = True
        return ret
