from django.test import TestCase

from .factories import ExtractionChecklistFactory, EnrollmentFactory, SubjectVisitFactory
from ba_namotswe.models import Appointment
from ba_namotswe.models.crf_metadata import CrfMetadata
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_constants.constants import NO


class TestBanamotsweRuleGroup(TestCase):

    def setUp(self):
        self.enrollment = EnrollmentFactory()
        self.appointments = Appointment.objects.filter(
            subject_identifier=self.enrollment.subject_identifier).orderby('visit_code')
        self.extraction_checklist = ExtractionChecklistFactory(subject_visit=self.subject_visit)

    def test_adherence_required(self):
        subject_visit = SubjectVisitFactory(appointment=self.appointments.get(visit_code='10'))
        self.extraction_checklist = ExtractionChecklistFactory(subject_visit=self.subject_visit)
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.adherencecounselling').count(), 1)

    def test_not_adherence_required(self):
        self.extraction_checklist.counselling_adhere = NO
        self.extraction_checklist.save()
        print(CrfMetadata.objects.filter(subject_identifier=self.enrollment.subject_identifier, model='ba_namotswe.adherencecounselling')[0].entry_status, '**********************************')
#         self.assertEqual(
#             CrfMetadata.objects.filter(
# #                 entry_status=NOT_REQUIRED,
#                 subject_identifier=self.enrollment.subject_identifier,
#                 model='ba_namotswe.adherencecounselling').count(), 1)
