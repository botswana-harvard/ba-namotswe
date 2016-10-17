from datetime import date
from django.test import TestCase

from edc_constants.constants import YES

from ba_namotswe.forms.treatment_form import TreatmentForm
from ba_namotswe.tests.factories.treatment_factory import TreatmentFactory


class TestTreatmentForm(TestCase):

    def setUp(self):
        """Setup data with all required fields for Treatment"""
        self.treatment = TreatmentFactory
        self.data = {
            'report_date': date(2016,10,13),
            'perinatal_infection': YES,
            'pmtct': YES,
            'pmtct_rx': 'AZT Monotherapy',
            'infant_prohylaxis': YES,
            'infant_prohylaxis_rx': 'AZT',
            'counseling': YES,
            'counseling_date': date(2016, 7, 7),
            'adherence_partner_rel': 'Mother',
            'adherence_partner_rel': None}

    def test_valid_form(self):
        """Test to verify whether form will submit"""
        form = TreatmentForm(data=self.data)
        self.assertTrue(form.is_valid())
