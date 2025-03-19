from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_dashboard, name='employee_dashboard'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('update_leave_status/<int:leave_id>/', views.update_leave_status, name='update_leave_status'),
    path('edit_leave/<int:leave_id>/', views.edit_leave, name='edit_leave'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('accounts/login/', views.login_redirect, name='login'),  # Custom view to handle the redirect
    # path('add_level_quota/', views.add_level_quota, name='add_level_quota'),
    path('add_report/', views.add_report, name='add_report'),
    path('edit_report/<int:report_id>/', views.edit_report, name='edit_report'),
    path('leave-quotas/', views.leave_quota_list, name='leave_quota_list'),
    path('edit-leave-quota/<int:pk>/', views.edit_leave_quota, name='edit_leave_quota'),
]
