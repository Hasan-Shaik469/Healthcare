from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Patient, Doctor, PatientDoctorMapping

admin.site.register(User, UserAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(PatientDoctorMapping)