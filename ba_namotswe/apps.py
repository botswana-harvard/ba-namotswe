from django.apps import AppConfig as DjangoAppConfig

from edc_base.apps import AppConfig as EdcBaseAppConfigParent
from edc_protocol.apps import AppConfig as EdcProtocolAppConfigParent
from edc_timepoint.apps import AppConfig as EdcTimepointAppConfigParent
from edc_appointment.apps import AppConfig as EdcAppointmentAppConfigParent
from edc_timepoint.timepoint import Timepoint
from edc_registration.apps import AppConfig as EdcRegistrationAppConfigParent
from edc_visit_tracking.apps import AppConfig as EdcVisitTrackingAppConfigParent


class AppConfig(DjangoAppConfig):
    name = 'ba_namotswe'


class EdcBaseAppConfig(EdcBaseAppConfigParent):
    institution = 'Botswana Harvard AIDS Institute Partnership'
    project_name = 'Ba Namotswe'


class EdcProtocolAppConfig(EdcProtocolAppConfigParent):
    enrollment_caps = {'ba_namotswe.enrollment': ('subject', -1)}  # {label_lower: (key, count)}


class EdcTimepointAppConfig(EdcTimepointAppConfigParent):
    timepoints = [
        Timepoint(
            model='ba_namotswe.appointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='CLOSED'
        )
    ]


class EdcRegistrationAppConfig(EdcRegistrationAppConfigParent):
    app_label = 'ba_namotswe'


class EdcAppointmentAppConfig(EdcAppointmentAppConfigParent):
    app_label = 'ba_namotswe'


class EdcVisitTrackingAppConfig(EdcVisitTrackingAppConfigParent):
    name = 'edc_visit_tracking'
    verbose_name = 'Edc Visit Tracking'
    visit_models = {'ba_namotswe': ('subject_visit', 'ba_namotswe.subjectvisit')}
