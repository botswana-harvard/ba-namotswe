import factory

from datetime import date, datetime
from django.utils import timezone

from edc_constants.constants import YES, NO

from ba_namotswe.models import Enrollment


class EnrollmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Enrollment

    dob = date(1988, 7, 7)
    gender = 'female'
    initial_visit_date = timezone.datetime.date(datetime.today())
    caregiver_relation = 'mother'
    weight_measured = YES
    weight = 50
    height_measured = YES
    height = 106
    hiv_diagnosis_date = None
    art_initiation_date = date(2016, 7, 7)
