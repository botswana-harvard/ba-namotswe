import factory

from django.utils import timezone

from ...models import Appointment


class AppointmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Appointment

    appt_datetime = timezone.now()
    best_appt_datetime = timezone.now()
    appt_close_datetime = timezone.now()
    subject_identifier = '084-10000001-4'
    visit_instance = '0'
