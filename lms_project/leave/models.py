from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    LEVEL_CHOICES = [
        ('Junior', 'Junior'),
        ('Mid', 'Mid'),
        ('Senior', 'Senior'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='Junior')
    
    def __str__(self):
        return f"{self.name} - {self.department}"


class Leave(models.Model):
    LEAVE_TYPES = [
        ('SL', 'SL'),  # Sick Leave
        ('CL', 'CL'),  # Casual Leave
        ('PL', 'PL'),  # Paid Leave
        ('LWP', 'LWP'), # Leave Without Pay
    ]
    
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=3, choices=LEAVE_TYPES)  
    reason = models.TextField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type}"


class LeaveQuota(models.Model):
    LEAVE_TYPES = [
        ('SL', 'SL'),
        ('CL', 'CL'),
        ('PL', 'PL'),
        ('LWP', 'LWP'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    year = models.IntegerField()
    sl_quota = models.IntegerField()
    pl_quota = models.IntegerField()
    cl_quota = models.IntegerField()
    def __str__(self):
        return f"{self.employee.name} - {self.year}"


class Report(models.Model):  # Corrected the model name to 'Report'
    LEAVE_TYPES = [
        ('SL', 'SL'),
        ('CL', 'CL'),
        ('PL', 'PL'),
        ('LWP', 'LWP'),
    ]
    
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    reportee_name = models.CharField(max_length=255)  # 'reportee_name' is correct here
    leave_type = models.CharField(max_length=3, choices=LEAVE_TYPES)  
    reason = models.TextField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_reports')

    def __str__(self):
        return f"{self.reportee_name} - {self.leave_type}"  # Use reportee_name from the Report model
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_hr_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
