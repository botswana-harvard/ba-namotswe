from django.apps import AppConfig as DjangoAppConfig

from edc_protocol.apps import AppConfig as EdcProtocolAppConfigParent
from edc_timepoint.apps import AppConfig as EdcTimepointAppConfigParent
from edc_timepoint.timepoint import Timepoint
from edc_registration.apps import AppConfig as EdcRegistrationAppConfigParent
from edc_visit_tracking.apps import AppConfig as EdcVisitTrackingAppConfigParent


class AppConfig(DjangoAppConfig):
    name = 'banamotswe'


class EdcProtocolAppConfig(EdcProtocolAppConfigParent):
    enrollment_caps = {'banamotswe.enrollment': ('subject', -1)}  # {label_lower: (key, count)}


class EdcTimepointAppConfig(EdcTimepointAppConfigParent):
    timepoints = [
        Timepoint(
            model='banamotswe.appointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='CLOSED'
        )
    ]


class EdcRegistrationAppConfig(EdcRegistrationAppConfigParent):
    app_label = 'edc_example'


class EdcVisitTrackingAppConfig(EdcVisitTrackingAppConfigParent):
    name = 'edc_visit_tracking'
    verbose_name = 'Edc Visit Tracking'
    visit_models = {'banamotswe': ('subject_visit', 'banamotswe.subjectvisit')}
