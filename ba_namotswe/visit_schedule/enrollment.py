from edc_visit_schedule.visit_schedule import VisitSchedule
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Crf

from .requistions_entries import visits

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

subject_visit_schedule_enrollment = VisitSchedule(
    name='subject_visit_schedule',
    verbose_name='Ba Namotswe Visit Schedule',
    app_label='ba_namotswe',
    visit_model='ba_namotswe.subjectvisit',
)

# add schedules
schedule_enrollment = Schedule(name='schedule-1', enrollment_model='ba_namotswe.enrollment')

# add visits to this schedule
interval = 4
for visit in visits:
    code, reqs = visit
    interval = interval + 4
    schedule_enrollment.add_visit(
        code=code,
        title='Visit {}'.format(code),
        timepoint=interval,
        base_interval=interval,
        requisitions=reqs,
        crfs=crfs)

subject_visit_schedule_enrollment.add_schedule(schedule_enrollment)
