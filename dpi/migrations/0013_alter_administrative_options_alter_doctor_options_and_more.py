# Generated by Django 5.1.3 on 2024-12-20 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0012_remove_administrative_email_remove_doctor_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrative',
            options={'ordering': ['-dateAdded']},
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'ordering': ['-dateAdded']},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'ordering': ['-dateAdded']},
        ),
        migrations.RemoveField(
            model_name='administrative',
            name='created',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='created',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='created',
        ),
        migrations.AlterField(
            model_name='administrative',
            name='dateAdded',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='dateAdded',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='dateAdded',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
