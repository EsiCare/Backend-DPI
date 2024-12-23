# Generated by Django 5.1.3 on 2024-12-20 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0013_alter_administrative_options_alter_doctor_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laborantin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('SSN', models.CharField(max_length=50, unique=True)),
                ('dateAdded', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-dateAdded'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('SSN', models.CharField(max_length=50, unique=True)),
                ('dateAdded', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-dateAdded'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Radiologist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('SSN', models.CharField(max_length=50, unique=True)),
                ('dateAdded', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-dateAdded'],
                'abstract': False,
            },
        ),
    ]
