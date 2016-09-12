from django.contrib import admin

from .admin_site import ba_namotswe_admin
from .models import (
    RegisteredSubject, SubjectVisit, Enrollment, Io, Abstraction, Treatment, ARTRegimen, Appointment)


ba_namotswe_admin.register(RegisteredSubject)
ba_namotswe_admin.register(Appointment)
ba_namotswe_admin.register(SubjectVisit)
ba_namotswe_admin.register(Enrollment)
ba_namotswe_admin.register(Abstraction)
ba_namotswe_admin.register(Treatment)
ba_namotswe_admin.register(Io)
ba_namotswe_admin.register(ARTRegimen)
