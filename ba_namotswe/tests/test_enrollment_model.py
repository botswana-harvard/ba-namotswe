from datetime import date
from django.test.testcases import TestCase
from django.utils import timezone

from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED

from ba_namotswe.models import Appointment, SubjectVisit, RequisitionMetadata, CrfMetadata, SubjectConsent

from .factories.enrollment_factory import EnrollmentFactory
from ba_namotswe.models.registered_subject import RegisteredSubject


class TestEnrollment(TestCase):

    def test_create_enrollment(self):
        """Assert enrollment creates subject consent and appointments."""
        enrollment = EnrollmentFactory()
        schedule = site_visit_schedules.get_schedule(enrollment._meta.label_lower)
        self.assertEqual(SubjectConsent.objects.all().count(), 1)
        self.assertGreater(Appointment.objects.all().count(), 0)
        self.assertEqual(Appointment.objects.all().count(), len(schedule.visits))

#     def test_create_enrollment_bad_dob(self):
#         """Assert enrollment creates subject consent and appointments."""
#         EnrollmentFactory(dob=date(1900, 1, 1))

    def test_subject_identifier(self):
        """Assert enrollment subject_identifier is updated after consent is created."""
        enrollment = EnrollmentFactory()
        self.assertIsNotNone(enrollment.subject_identifier)
        SubjectConsent.objects.get(subject_identifier=enrollment.subject_identifier)
        RegisteredSubject.objects.get(subject_identifier=enrollment.subject_identifier)

    def test_subject_consent_attrs(self):
        """Assert attrs from enrollment match subject_consent."""
        enrollment = EnrollmentFactory()
        subject_consent = SubjectConsent.objects.get(subject_identifier=enrollment.subject_identifier)
        subject_consent.dob = enrollment.dob
        subject_consent.initials = enrollment.initials
        subject_consent.consent_datetime = enrollment.report_datetime
        subject_consent.gender = enrollment.gender

    def test_registered_subject_attrs(self):
        """Assert attrs from enrollment match registered_subject."""
        enrollment = EnrollmentFactory()
        registered_subject = RegisteredSubject.objects.get(subject_identifier=enrollment.subject_identifier)
        registered_subject.dob = enrollment.dob
        registered_subject.initials = enrollment.initials
        registered_subject.consent_datetime = enrollment.report_datetime
        registered_subject.gender = enrollment.gender

    def test_create_subject_visit(self):
        """Assert subject visit creates metadata."""
        EnrollmentFactory()
        appointment = Appointment.objects.all().order_by('visit_code').first()
        SubjectVisit.objects.create(
            appointment=appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED,
        )
        schedule = site_visit_schedules.get_schedule(appointment.schedule_name)
        visit = schedule.get_visit(appointment.visit_code)
        self.assertGreater(CrfMetadata.objects.all().count(), 0)
        self.assertEqual(CrfMetadata.objects.all().count(), len(visit.crfs))
        self.assertGreater(RequisitionMetadata.objects.all().count(), 0)
        self.assertEqual(RequisitionMetadata.objects.all().count(), len(visit.requisitions))
