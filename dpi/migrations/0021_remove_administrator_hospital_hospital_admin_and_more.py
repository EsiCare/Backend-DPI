# Generated by Django 5.1.3 on 2024-12-27 13:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0020_administrator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administrator',
            name='hospital',
        ),
        migrations.AddField(
            model_name='hospital',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_hospitals', to='dpi.administrator'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.CharField(default='paitent adress', max_length=200),
        ),
    ]