# Generated by Django 5.1.3 on 2024-12-29 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0023_alter_patient_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='care',
            name='dpi',
        ),
        migrations.RemoveField(
            model_name='dpi',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='dpi',
        ),
        migrations.RemoveField(
            model_name='test',
            name='dpi',
        ),
        migrations.RemoveField(
            model_name='medicalcondition',
            name='dpi',
        ),
        migrations.RemoveField(
            model_name='scan',
            name='test',
        ),
        migrations.DeleteModel(
            name='Bloodwork',
        ),
        migrations.DeleteModel(
            name='Care',
        ),
        migrations.DeleteModel(
            name='prescription',
        ),
        migrations.DeleteModel(
            name='Dpi',
        ),
        migrations.DeleteModel(
            name='MedicalCondition',
        ),
        migrations.DeleteModel(
            name='Scan',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]
