from datetime import date, datetime
from django.test import TestCase
from django import forms
from edc_constants.constants import YES, NO
from ba_namotswe.forms.enrollment_form import EnrollmentForm
from ba_namotswe.tests.factories.enrollment_factory import EnrollmentFactory
from ba_namotswe.tests.factories.registered_subject_factory import RegisteredSubjectFactory


class TestEnrollment(TestCase):

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
        form = EnrollmentForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_record_number_provided(self):
        """Test to see if record number provided"""
        form = EnrollmentForm(data=self.data)
        self.assertNotIn(
            'You should provide record number',
            form.errors.get('record_number', []))

    def test_record_number_provided_valid(self):
        """Test to see if valid record number is provided"""
        form = EnrollmentForm(data=self.data)
        self.assertNotIn(
            'You provided wrong record number',
            form.errors.get('record_number', []))

    def test_date_of_birth_provided(self):
        """Test to see if valid date_of_birth is provided"""
        form = EnrollmentForm(data=self.data)
        self.assertNotIn(
            'You provided valid dob',
            form.errors.get('date_of_birth', []))

    def test_date_of_birth_provided_not_valid(self):
        """Test to see if valid date_of_birth is provided"""
        form = EnrollmentForm(data=self.data)
        self.assertNotIn(
            'You provided invalid dob, please correct',
            form.errors.get('date_of_birth', []))

    def test_right_gender_provided(self):
        """Test to see if correct gender is provided"""
        form = EnrollmentForm(data=self.data)
        self.assertNotIn(
            'You provided correct sex, please correct',
            form.errors.get('gender', []))

    def test_gender_is_provided(self):
        """Test to see if gender is provided"""
        form = EnrollmentForm(data=self.data)
        self.assertNotIn(
            'You provided sex',
            form.errors.get('gender', []))

    def test_caretaker_relation(self):
        """Test to see who the caretaker is """
        form = EnrollmentForm(data=self.data)
        self.assertNotIn(
            'You provided the caretaker as other',
            form.errors.get('caregiver_relation_other', []))

    def test_caretaker_relation_is(self):
        """Test to see who the caretaker is """
        form = EnrollmentForm(data=self.data)
        self.assertNotIn(
            'You provided the caretaker as other',
            form.errors.get('caregiver_relation_other', []))

    def test_if_weight_provided(self):
        """Test to see if weight is given """
        form = EnrollmentForm(data=self.data)
        self.assertNotIn(
            'You provided the weight',
            form.errors.get('weight', []))

    def test_if_height_provided(self):
        """Test to see if height is given """
        form = EnrollmentForm(data=self.data)
        self.assertNotIn(
            'You provided the height',
            form.errors.get('height', []))

    def test_if_anti_retroviral_treatment_given(self):
        """Test to see if ART is given """
        form = EnrollmentForm(data=self.data)
        self.assertNotIn(
            'ART provided',
            form.errors.get('height', []))

