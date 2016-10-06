import factory

from datetime import date
from .models import RegisteredSubject
from edc_constants.constants import FEMALE


class RegisteredSubjectFactory(factory.DjangoModelFactory):

    class Meta:
        model = RegisteredSubject

    first_name = 'Nametso'

    last_name = 'Masire'

    initials = 'NM'

    dob = date(1988, 7, 7)

    is_dob_estimated = 'No'

    gender = FEMALE
