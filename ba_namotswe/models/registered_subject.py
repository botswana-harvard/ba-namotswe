from edc_base.model.models import BaseUuidModel
from edc_registration.model_mixins import RegisteredSubjectModelMixin

from simple_history.models import HistoricalRecords


class RegisteredSubject(RegisteredSubjectModelMixin, BaseUuidModel):

    history = HistoricalRecords()

    class Meta:
        app_label = 'ba_namotswe'
