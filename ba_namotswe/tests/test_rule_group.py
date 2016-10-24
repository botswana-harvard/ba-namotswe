from django.test import TestCase

from .factories import ExtractionChecklistFactory, EnrollmentFactory, SubjectVisitFactory
from ba_namotswe.models import Appointment
from ba_namotswe.models.crf_metadata import CrfMetadata
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_constants.constants import NO, YES


class TestBanamotsweRuleGroup(TestCase):

    def setUp(self):
        self.enrollment = EnrollmentFactory()
        self.appointments1, self.appointments2 = Appointment.objects.filter(
            subject_identifier=self.enrollment.subject_identifier).order_by('visit_code')
        self.subject_visit = SubjectVisitFactory(appointment=self.appointments1)
        self.extraction_checklist = ExtractionChecklistFactory(subject_visit=self.subject_visit)

    def test_adherence_required(self):
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.adherencecounselling').count(), 1)

    def test_not_adherence_required(self):
        self.extraction_checklist.counselling_adhere = NO
        self.extraction_checklist.save()
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.adherencecounselling').count(), 1)

    def test_art_regimen_required(self):
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.artregimen').count(), 1)

    def test_not_art_regimen_required(self):
        self.extraction_checklist.arv_changes = NO
        self.extraction_checklist.save()
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.artregimen').count(), 1)

    def test_assessment_history_required(self):
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.assessmenthistory').count(), 1)

    def test_not_assessment_history_required(self):
        self.extraction_checklist.assessment_history = YES
        self.extraction_checklist.save()
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.assessmenthistory').count(), 1)

    def test_not_extraction_required(self):
        self.extraction_checklist.extraction = NO
        self.extraction_checklist.save()
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.extraction').count(), 1)

    def test_extraction_required(self):
        self.extraction_checklist.extraction = YES
        self.extraction_checklist.save()
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.extraction').count(), 1)

    def test_pregnancy_required(self):
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.pregnancyhistory').count(), 1)

    def test_not_pregnancy_required(self):
        self.extraction_checklist.preg_diagnosis = NO
        self.extraction_checklist.save()
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.pregnancyhistory').count(), 1)

    def test_oi_required(self):
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.oi').count(), 1)

    def test_oi_not_required(self):
        self.extraction_checklist.oi_diagnosis = NO
        self.extraction_checklist.save()
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.oi').count(), 1)

    def test_tb_history_required(self):
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.tbhistory').count(), 1)

    def test_tb_history_not_required(self):
        self.extraction_checklist.tb_diagnosis = NO
        self.extraction_checklist.save()
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.tbhistory').count(), 1)

    def test_transfer_history_required(self):
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.transferhistory').count(), 1)

    def test_transfer_history_not_required(self):
        self.extraction_checklist.transfer = NO
        self.extraction_checklist.save()
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.transferhistory').count(), 1)

    def test_treatment_required(self):
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.treatment').count(), 1)

    def test_treatment_not_required(self):
        self.extraction_checklist.treatment = NO
        self.extraction_checklist.save()
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.treatment').count(), 1)

    def test_death_required(self):
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.death').count(), 1)

    def test_death_not_required(self):
        self.extraction_checklist.death = NO
        self.extraction_checklist.save()
        self.assertEqual(
            CrfMetadata.objects.filter(
                entry_status=NOT_REQUIRED,
                subject_identifier=self.enrollment.subject_identifier,
                model='ba_namotswe.death').count(), 1)
