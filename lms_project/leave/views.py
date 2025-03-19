from django.shortcuts import render, redirect
from django.http import HttpResponse

import leave
from .models import Leave, LeaveQuota, Employee
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib.auth import views as auth_views
# Dashboard for Employees

# Apply Leave
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Leave
from datetime import datetime

def apply_leave(request):
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        reason = request.POST.get('reason')
        start_date_str = request.POST.get('start_date')  # String from form
        end_date_str = request.POST.get('end_date')    # String from form

        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # Calculate total days (difference in days)
        total_days = (end_date - start_date).days

        # Create a Leave instance (save to database)
        leave = Leave(
            leave_type=leave_type,
            reason=reason,
            start_date=start_date,
            end_date=end_date,
            total_days=total_days,
            status='pending',  # Default status
            employee=request.user.employee  # Assuming the logged-in user has an Employee instance
        )
        leave.save()

        # Redirect or provide a response
        return redirect('employee_dashboard')  # Redirect to a dashboard or a different page

    return render(request, 'apply_leave.html')

@login_required
def update_leave_status(request, leave_id):
    leave = Leave.objects.get(id=leave_id)
    if request.user.employee.department == 'HR' or request.user.employee.id == leave.employee.id:
        if request.method == 'POST':
            new_status = request.POST['status']
            leave.status = new_status
            leave.approved_by = request.user.employee
            leave.save()
            return redirect('admin_dashboard')  # Assuming an admin dashboard page exists
    return HttpResponse("Unauthorized", status=403)
@login_required
def admin_dashboard(request):
    # Get all leave requests for employees who report to the logged-in admin
    # Assuming 'request.user' is an admin or manager who has access to reportees
    reportees_leaves = Leave.objects.filter(approved_by=request.user)  # Adjust if needed based on relationships

    return render(request, 'admin_dashboard.html', {'reportees_leaves': reportees_leaves})
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def login_redirect(request):
    if request.user.is_authenticated:
        
        return redirect('employee_dashboard')
    else:

        return auth_views.LoginView.as_view()(request) # type: ignore
from django.shortcuts import render, get_object_or_404, redirect
from .models import Leave
from .forms import LeaveForm  # type: ignore # Assuming you have a form to handle the leave edit

# Employee Dashboard View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Leave


from .models import Leave, Report

@login_required
def employee_dashboard(request):
    employee = request.user.employee  # Ensure employee profile is set up
    
    # Calculate leave balances (example total allowed leave balances)
    total_pl = 8  # Example total allowed PL leave
    total_cl = 3  # Example total allowed CL leave
    total_sl = 5  # Example total allowed SL leave
    
    # Calculate used leave for each type
    pl_used = Leave.objects.filter(employee=employee, leave_type='PL').filter(status='approved').count()
    cl_used = Leave.objects.filter(employee=employee, leave_type='CL').filter(status='approved').count()
    sl_used = Leave.objects.filter(employee=employee, leave_type='SL').filter(status='approved').count()
    
    leave_balance = {
        'PL': total_pl - pl_used,
        'CL': total_cl - cl_used,
        'SL': total_sl - sl_used,
    }
    
    # Get the leaves taken by the employee
    leaves = Leave.objects.filter(employee=employee)
    
    # Get the reports related to the employee (assuming there's a relation between report and employee)
    reports = Report.objects.all()  # Adjust the filter as needed
    
    # Pass both leaves and reports to the template
    return render(request, 'employee_dashboard.html', {'leaves': leaves, 'leave_balance': leave_balance, 'reports': reports})

# Edit Leave View
# leave/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Leave
from .forms import LeaveForm  # Import LeaveForm instead of EditLeaveForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Leave
from .forms import LeaveForm  # Assuming LeaveForm is a ModelForm for Leave model

def edit_leave(request, leave_id):
    # Get the leave object by ID or return 404 if not found
    leave = get_object_or_404(Leave, id=leave_id)

    # If the request method is POST, it means the form is being submitted
    if request.method == 'POST':
        # Bind the form with the submitted data, and the current leave instance
        form = LeaveForm(request.POST, instance=leave)

        # Check if the form is valid
        if form.is_valid():
            form.save()  # Save the changes to the database
            return redirect('employee_dashboard')  # Redirect back to the dashboard after saving
    else:
        # If the form isn't submitted, pre-fill it with the current leave instance data
        form = LeaveForm(instance=leave)

    # Render the form on the edit_leave page
    return render(request, 'edit_leave.html', {'form': form, 'leave': leave})

from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportForm

def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')  # Or wherever you want to redirect after saving
    else:
        form = ReportForm()

    return render(request, 'add_report.html', {'form': form})
from django.shortcuts import render
from .models import Report

from django.shortcuts import render, get_object_or_404, redirect
from .models import Report
from .forms import ReportForm

def edit_report(request, report_id):
    # Get the report object by ID or return 404 if not found
    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()  # Save the changes to the report
            return redirect('employee_dashboard')  # Redirect back to the dashboard
    else:
        form = ReportForm(instance=report)

    return render(request, 'edit_report.html', {'form': form, 'report': report})
from django.shortcuts import render, redirect
from .models import LeaveQuota, Employee
from .forms import LeaveQuotaForm
from django.contrib.auth.decorators import user_passes_test

# Check if the user is HR or Admin
def leave_quota_list(request):
    leave_quotas = LeaveQuota.objects.all()
    return render(request, 'leave_quota_list.html', {'leave_quotas': leave_quotas})

# View to edit leave quota
def edit_leave_quota(request, pk):
    leave_quota = get_object_or_404(LeaveQuota, pk=pk)
    if request.method == 'POST':
        form = LeaveQuotaForm(request.POST, instance=leave_quota)
        if form.is_valid():
            form.save()
            return redirect('leave_quota_list')
    else:
        form = LeaveQuotaForm(instance=leave_quota)
    return render(request, 'edit_leave_quota.html', {'form': form})
