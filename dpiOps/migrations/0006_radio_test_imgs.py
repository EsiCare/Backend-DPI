# Generated by Django 5.1.4 on 2024-12-31 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpiOps', '0005_nurse_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='radio_test',
            name='imgs',
            field=models.JSONField(default=[]),
        ),
    ]