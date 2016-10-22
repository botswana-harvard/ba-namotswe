from django.test import TestCase
from datetime import date, datetime

from edc_constants.constants import YES
from ba_namotswe.forms.subject_visit_form import SubjectVisitForm
from ba_namotswe.tests.factories.enrollment_factory import EnrollmentFactory
from ba_namotswe.models.appointment import Appointment


class TestSubjectVisitForm(TestCase):

    def setUp(self):

        self.data = {
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
        EnrollmentFactory()
        self.data['appointment'] = Appointment.objects.all().order_by('visit_code').first()
        form = SubjectVisitForm(data=self.data)
        self.assertTrue(form.is_valid())
