from django.contrib import admin

from ba_namotswe.models import (
    RegisteredSubject, SubjectVisit, Enrollment, Io, Abstraction, Treatment, ARTRegimen, Appointment)


admin.site.register(RegisteredSubject)
admin.site.register(Appointment)
admin.site.register(SubjectVisit)
admin.site.register(Enrollment)
admin.site.register(Abstraction)
admin.site.register(Treatment)
admin.site.register(Io)
admin.site.register(ARTRegimen)
