import factory

from datetime import date
from ba_namotswe.models import Treatment
from edc_constants.constants import YES


class TreatmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Treatment

    perinatal_infection = YES

    pmtct = YES

    pmtct_rx = 'AZT Monotherapy'

    infant_prohylaxis = YES

    infant_prohylaxis_rx = 'AZT'

    counseling = YES

    counseling_date = date(2016, 7, 7)

    adherence_partner_rel = 'Mother'
