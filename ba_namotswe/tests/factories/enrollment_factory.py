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
    weight_measured = YES
    weight = random.choice(range(35, 60))
    height_measured = YES
    height = random.choice(range(100, 120))
    hiv_diagnosis_date = None
    art_initiation_date = parse(fake.date())
