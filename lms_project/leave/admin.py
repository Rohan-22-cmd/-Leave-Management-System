from django.contrib import admin
from .models import Employee, Leave, LeaveQuota, Report

admin.site.register(Employee)
admin.site.register(Leave)
admin.site.register(LeaveQuota)
admin.site.register(Report)
