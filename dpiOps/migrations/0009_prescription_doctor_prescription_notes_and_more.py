# Generated by Django 5.1.4 on 2025-01-01 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0024_remove_care_dpi_remove_dpi_patient_and_more'),
        ('dpiOps', '0008_prescriptionentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescriptions', to='dpi.doctor'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='notes',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='prescription',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='dpi.patient'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='validationDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]