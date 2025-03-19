# leave/forms.py
from django import forms
from .models import Leave, Report

from django import forms
from .models import Leave

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type', 'reason', 'start_date', 'end_date', 'status']

from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reportee_name', 'leave_type', 'reason', 'start_date', 'end_date',  'status']

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    status = forms.ChoiceField(choices=STATUS_CHOICES)
from django import forms
from .models import LeaveQuota, Employee

class LeaveQuotaForm(forms.ModelForm):
    class Meta:
        model = LeaveQuota
        fields = ['employee', 'sl_quota', 'pl_quota', 'cl_quota']
