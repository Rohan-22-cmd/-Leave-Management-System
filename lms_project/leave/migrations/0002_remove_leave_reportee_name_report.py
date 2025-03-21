# Generated by Django 5.1.3 on 2025-03-19 08:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='reportee_name',
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportee_name', models.CharField(max_length=255)),
                ('leave_type', models.CharField(choices=[('SL', 'SL'), ('CL', 'CL'), ('PL', 'PL'), ('LWP', 'LWP')], max_length=3)),
                ('reason', models.TextField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_days', models.IntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_reports', to='leave.employee')),
            ],
        ),
    ]
