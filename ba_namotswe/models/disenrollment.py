from edc_base.model.models import BaseUuidModel
from edc_visit_schedule.model_mixins import DisenrollmentModelMixin


class Disenrollment(DisenrollmentModelMixin, BaseUuidModel):

    class Meta:
        visit_schedule_name = 'visit_schedule'
