import factory
import random
from dateutil.parser import parse
from django.utils import timezone
from faker import Faker

from edc_constants.constants import YES

from ba_namotswe.models import Enrollment

fake = Faker()


class EnrollmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Enrollment

    initials = ''.join([name[0] for name in fake.name().split(' ')])
    dob = parse(fake.date())
    gender = random.choice(['M', 'F'])
    initial_visit_date = timezone.now()
    caregiver_relation = 'mother'
