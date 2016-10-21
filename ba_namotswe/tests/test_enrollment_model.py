from datetime import datetime

from django.test.testcases import TestCase

from ba_namotswe.models import Appointment, SubjectIdentifier, SubjectVisit
from ba_namotswe.tests.factories.enrollment_factory import EnrollmentFactory
from ba_namotswe.models.requisition_meta_data import RequisitionMetadata, CrfMetadata


class TestEnrollment(TestCase):

    def setUp(self):
        for identifier in ['1001243-1', '1001243-2', '1001243-3', '1001243-4', '1001243-5', '1001243-6']:
            SubjectIdentifier.objects.create(
                subject_identifier=identifier
            )

    def test_identifiers(self):
        self.assertEqual(6, SubjectIdentifier.objects.all().count())

    def test_create_enrollment_post_save_appointments(self):
        EnrollmentFactory()
        self.assertEqual(Appointment.objects.all().count(), 2)

    def test_create_subject_visit_and_metadata_at_enrollment(self):
        EnrollmentFactory()
        appointment = Appointment.objects.all().order_by('visit_code').first()

        SubjectVisit.objects.create(
            appointment=appointment,
            report_datetime=datetime.today(),
            reason='scheduled',
        )
        self.assertEqual(CrfMetadata.objects.all().count(), 0)
        self.assertEqual(RequisitionMetadata.objects.all().count(), 1)

    def test_get_requisitions(self):
        EnrollmentFactory()
        appointment = Appointment.objects.all().order_by('visit_code').first()

        SubjectVisit.objects.create(
            appointment=appointment,
            report_datetime=datetime.today(),
            reason='scheduled',
        )
        self.assertEqual(CrfMetadata.objects.all().count(), 0)
        self.assertEqual(RequisitionMetadata.objects.all().count(), 1)
