
from edc_visit_schedule.visit import Requisition

from ba_namotswe.lab_profiles import hiv_diagnostics_panel


requisitions_hvs = (
    Requisition(show_order=10, model='ba_namotswe.SubjectRequisition', panel=hiv_diagnostics_panel),)

visits = [('1.0', requisitions_hvs), ('2.0', requisitions_hvs)]
