from django.test import TestCase
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from edc_constants.constants import YES
from ba_namotswe.forms.enrollment_form import EnrollmentForm
from ba_namotswe.tests.factory.factory import RegisteredSubjectFactory


class TestEnrollmentForm(TestCase):

    def setUp(self):
        """Setup data"""
        self.registered_subject = RegisteredSubjectFactory()

        self.data = {
            'registered_subject': self.registered_subject.id,
            'report_datetime': datetime.now(),
            'is_eligible': True,
            'initial_visit_date': date.today() - relativedelta(years=3),
            'caregiver_relation': 'mother',
            #'caregiver_relation_other': 'Wife',
            'weight_measured': YES,
            'weight': 200,
            'height_measured': YES,
            'height': 50,
            'art_initiation_date': date.today()}

    def test_valid_form(self):
        """Test to verify whether form will submit"""
        form = EnrollmentForm(data=self.data)
        print(form.errors)
        self.assertTrue(form.is_valid())
