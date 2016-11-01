import pytz

from datetime import datetime

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings

from edc_appointment.apps import AppConfig as EdcAppointmentAppConfigParent
from edc_base.apps import AppConfig as EdcBaseAppConfigParent
from edc_consent.apps import AppConfig as EdcConsentAppConfigParent
from edc_consent.consent_config import ConsentConfig
from edc_identifier.apps import AppConfig as EdcIdentifierAppConfigParent
from edc_lab.apps import AppConfig as EdcLabAppConfig
from edc_metadata.apps import AppConfig as EdcMetaDataAppConfigParent
from edc_protocol.apps import AppConfig as EdcProtocolAppConfigParent
from edc_registration.apps import AppConfig as EdcRegistrationAppConfigParent
from edc_timepoint.apps import AppConfig as EdcTimepointAppConfigParent
from edc_timepoint.timepoint import Timepoint
from edc_visit_tracking.apps import AppConfig as EdcVisitTrackingAppConfigParent

tz = pytz.timezone(settings.TIME_ZONE)


class AppConfig(DjangoAppConfig):
    name = 'ba_namotswe'

    def ready(self):
        from .models import signals


class EdcRegistrationAppConfig(EdcRegistrationAppConfigParent):
    app_label = 'ba_namotswe'


class EdcIdentifierAppConfig(EdcIdentifierAppConfigParent):
    identifier_prefix = '084'


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


class EdcConsentAppConfig(EdcConsentAppConfigParent):
    consent_configs = [
        ConsentConfig(
            'ba_namotswe.subjectconsent',
            version='1',
            start=datetime(2016, 5, 1, 0, 0, 0),
            end=datetime(2017, 10, 30, 0, 0, 0),
            age_min=16,
            age_is_adult=18,
            age_max=64,
            gender=['M', 'F']
        )
    ]


class EdcAppointmentAppConfig(EdcAppointmentAppConfigParent):
    app_label = 'ba_namotswe'


class EdcVisitTrackingAppConfig(EdcVisitTrackingAppConfigParent):
    visit_models = {'ba_namotswe': ('subject_visit', 'ba_namotswe.subjectvisit')}


class EdcLabAppConfig(EdcLabAppConfig):
    app_label = 'ba_namotswe'
    requisition = 'ba_namotswe.subjectrequisition'


class EdcMetaDataAppConfig(EdcMetaDataAppConfigParent):
    model_attrs = [('ba_namotswe', 'crfmetadata'), ('ba_namotswe', 'requisitionmetadata')]
    reason_field = {'ba_namotswe.subjectvisit': 'reason'}
    app_label = 'ba_namotswe'
