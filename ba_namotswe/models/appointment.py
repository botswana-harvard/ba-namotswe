from edc_base.model.models.base_uuid_model import BaseUuidModel

from edc_consent.model_mixins import RequiresConsentMixin

from edc_appointment.model_mixins import AppointmentModelMixin


class Appointment(AppointmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    class Meta(AppointmentModelMixin.Meta):
        consent_model = 'ba_namotswe.subjectconsent'
        app_label = 'ba_namotswe'
