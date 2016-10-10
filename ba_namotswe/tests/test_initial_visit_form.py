from django.test import TestCase
from datetime import date, datetime

from edc_constants.constants import YES, NO

from ba_namotswe.forms.initial_visit_form import SubjectVisitForm
from ba_namotswe.tests.factories.registered_subject_factory import RegisteredSubjectFactory


class TestSubjectVistForm(TestCase):

    def setUp(self):
        self.registered_subject = RegisteredSubjectFactory()
        self.data = {
            'registered_subject': self.registered_subject.id,
            'report_datetime': datetime.now(),
            'is_eligible': True,
            'initial_visit_date': date.today(),
            'caregiver_relation': 'mother',
            'caregiver_relation_other': 'Wife',
            'weight_measured': YES,
            'height_measured': YES,
            'art_initiation_date': date.today()}

    def test_valid_form(self):
        """Test to verify that enrollment form will submit"""
        form = SubjectVisitForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_report_datetime_provided(self):
        """Test to see if participant initial visit time provided"""
        form = SubjectVisitForm(data=self.data)
        self.assertNotIn(
            'You should provide the correct report time for initial visit',
            form.errors.get('report_datetime', []))
