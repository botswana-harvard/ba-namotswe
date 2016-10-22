from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_schedule.visit_schedule import VisitSchedule
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Crf, Requisition

from .lab_profiles import hiv_diagnostics_panel

crfs = (
    Crf(show_order=10, model='ba_namotswe.abstraction'),
    Crf(show_order=20, model='ba_namotswe.adherencecounselling'),
    Crf(show_order=30, model='ba_namotswe.artregimen'),
    Crf(show_order=40, model='ba_namotswe.arvhistory'),
    Crf(show_order=50, model='ba_namotswe.assessmenthistory'),
    Crf(show_order=60, model='ba_namotswe.collecteddata'),
    Crf(show_order=70, model='ba_namotswe.pregnancyhistory'),
    Crf(show_order=80, model='ba_namotswe.tbhistory'),
    Crf(show_order=90, model='ba_namotswe.transferhistory'),
    Crf(show_order=100, model='ba_namotswe.treatment'),
    Crf(show_order=110, model='ba_namotswe.death', required=False),
)

requisitions = (
    Requisition(show_order=10, model='ba_namotswe.SubjectRequisition', panel=hiv_diagnostics_panel),
)

visit_schedule = VisitSchedule(
    name='visit_schedule',
    verbose_name='Ba Namotswe Visit Schedule',
    app_label='ba_namotswe',
    visit_model='ba_namotswe.subjectvisit',
)

# add schedules
schedule = Schedule(name='schedule', enrollment_model='ba_namotswe.enrollment')

# add visits to this schedule
for i in range(1, 3):
    visit_code = code = str(i * 10)
    schedule.add_visit(
        code=visit_code,
        title='Visit {}'.format(visit_code),
        timepoint=i * 10,
        base_interval=i * 10,
        requisitions=requisitions,
        crfs=crfs)

visit_schedule.add_schedule(schedule)

site_visit_schedules.register(visit_schedule)
