from edc_base.model.models.base_uuid_model import BaseUuidModel

from edc_consent.model_mixins import RequiresConsentMixin
from edc_appointment.model_mixins import AppointmentModelMixin


class Appointment(AppointmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    class Meta:
        app_label = 'ba_namotswe'

    @property
    def str_pk(self):
        return str(self.pk)

    @property
    def subject_visit(self):
        from .subject_visit import SubjectVisit
        try:
            return SubjectVisit.objects.get(appointment=self)
        except SubjectVisit.DoesNotExist:
            return None
