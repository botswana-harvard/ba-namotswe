from edc_visit_schedule.visit_schedule import VisitSchedule
from edc_visit_schedule.schedule import Schedule

from .requistions_entries import visits

crfs = (
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
