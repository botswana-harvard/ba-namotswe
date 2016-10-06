from django.test import TestCase
from .forms import EnrollmentForm
from .factory import RegisteredSubjectFactory
from datetime import datetime, date
from edc_constants.constants import YES


class TestEnrollmentForm(TestCase):

    def setUp(self):
        """Setup data"""
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
        """Test to verify whether form will submit"""
        form = EnrollmentForm(data=self.data)
        print(form.errors)
        self.assertTrue(form.is_valid())
