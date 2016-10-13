from edc_registration.model_mixins import RegisteredSubjectModelMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel


class RegisteredSubject(RegisteredSubjectModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'ba_namotswe'
