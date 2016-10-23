import factory
from django.utils import timezone

from .appointment_factory import AppointmentFactory

from ...models import SubjectVisit
from edc_visit_tracking.constants import SCHEDULED


class SubjectVisitFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectVisit

    report_datetime = timezone.now()
    appointment = factory.SubFactory(AppointmentFactory)
    info_source = "participant"
    study_status = SCHEDULED
    reason = SCHEDULED
