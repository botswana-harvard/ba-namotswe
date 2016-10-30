from datetime import date, datetime
from django.test import TestCase

from dateutil.relativedelta import relativedelta

from edc_constants.constants import YES, MALE

from ba_namotswe.forms import EnrollmentForm


class TestEnrollment(TestCase):

    def setUp(self):

        self.data = {
            'initials': 'AH',
            'dob': date(1990, 12, 16),
            'gender': MALE,
            'report_datetime': datetime.now(),
            'is_eligible': True,
            'initial_visit_date': date.today() - relativedelta(years=4),
            'weight_measured': YES,
            'weight': 100,
            'height_measured': YES,
            'height': 140,
            'art_initiation_date': date.today()}

    def test_valid_form(self):
        """Test to verify that enrollment form will submit"""
        form = EnrollmentForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_initial_visit_date_validation_before_date(self):
        """Test to verify that validation for initial visit date works"""
        self.data['initial_visit_date'] = date(1990, 1, 1)
        form = EnrollmentForm(data=self.data)
        self.assertIn(
            'Initial visit date should come after January 1st, 2002',
            form.errors.get('initial_visit_date', []))

    def test_initial_visit_date_validation_after_date(self):
        """Test to verify that validation for initial visit date works"""
        self.data['initial_visit_date'] = date(2016, 10, 10)
        form = EnrollmentForm(data=self.data)
        self.assertIn(
            'Initial visit date should come before June 1st, 2016',
            form.errors.get('initial_visit_date', []))
