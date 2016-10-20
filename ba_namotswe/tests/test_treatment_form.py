from datetime import date, datetime
from django.test import TestCase

from edc_constants.constants import YES

from ba_namotswe.forms.treatment_form import TreatmentForm
from ba_namotswe.tests.factories.treatment_factory import TreatmentFactory


class TestTreatmentForm(TestCase):

    def setUp(self):
        """Setup data with all required fields for Treatment"""
        self.data = {
            'report_datetime': datetime(2016, 10, 13, 16, 16, 16),
            'art_history': 'Regimen 3',
            'perinatal_infection': YES,
            'pmtct': YES,
            'pmtct_rx': 'azt_monotherapy',
            'infant_prohylaxis': YES,
            'infant_prohylaxis_rx': 'azt',
            'counseling': YES,
            'counseling_date': date(2016, 7, 7),
            'adherence_partner_rel': 'Mother',
            'adherence_partner_rel': None}

    def test_valid_form(self):
        """Test to verify whether treatment form will submit"""
        form = TreatmentForm(data=self.data)
        print('************TREATMENT****FORM****ERRORS*************')
        print(form.errors)
        self.assertTrue(form.is_valid())
