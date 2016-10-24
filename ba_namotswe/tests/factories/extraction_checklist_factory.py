import factory

from edc_constants.constants import YES

from ba_namotswe.models import ExtractionChecklist


class ExtractionChecklistFactory(factory.DjangoModelFactory):

    class Meta:
        model = ExtractionChecklist

    arv_changes = YES
    tb_diagnosis = YES
    oi_diagnosis = YES
    preg_diagnosis = YES
    counselling_adhere = YES
    transfer = YES
    treatment = YES
    assessment_history = YES
    extraction = YES
    death = YES
