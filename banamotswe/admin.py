from django.contrib import admin

from banamotswe.models import RegisteredSubject, SubjectVisit, Enrollment, CrfOne


admin.register(RegisteredSubject)
admin.register(SubjectVisit)
admin.register(Enrollment)
admin.register(CrfOne)
