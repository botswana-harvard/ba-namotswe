from django.test import TestCase

from .factories import CollectedDataFactory, EnrollmentFactory, SubjectVisitFactory
from ba_namotswe.models import Appointment
from ba_namotswe.models.crf_metadata import CrfMetadata
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_constants.constants import NO


class TestBanamotsweRuleGroup(TestCase):

    def setUp(self):
        self.enrollment = EnrollmentFactory()
        self.appointment1, self.appointment2 = Appointment.objects.filter(subject_identifier=self.enrollment.subject_identifier)
        self.subject_visit = SubjectVisitFactory(appointment=self.appointment1)
        self.collected_data = CollectedDataFactory(subject_visit=self.subject_visit)

    def test_adherence_required(self):
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.adherencecounselling').count(), 1)

    def test_not_adherence_required(self):
        self.collected_data.counselling_adhere = NO
        self.collected_data.save()
        print(CrfMetadata.objects.filter(subject_identifier=self.enrollment.subject_identifier, model='ba_namotswe.adherencecounselling')[0].entry_status, '**********************************')
#         self.assertEqual(
#             CrfMetadata.objects.filter(
# #                 entry_status=NOT_REQUIRED,
#                 subject_identifier=self.enrollment.subject_identifier,
#                 model='ba_namotswe.adherencecounselling').count(), 1)
