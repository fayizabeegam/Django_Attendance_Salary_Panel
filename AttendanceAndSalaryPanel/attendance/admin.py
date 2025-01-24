from django.contrib import admin
from attendance.models import*
# Register your models here.
admin.site.register(Employee)
admin.site.register(AttendanceMonth)
admin.site.register(AttendanceSheet)
admin.site.register(Attendance)