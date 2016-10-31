from edc_base.model.models import BaseUuidModel
from edc_registration.model_mixins import RegisteredSubjectModelMixin


class RegisteredSubject(RegisteredSubjectModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'ba_namotswe'
