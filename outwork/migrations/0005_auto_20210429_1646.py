# Generated by Django 3.1.5 on 2021-04-29 20:46

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outwork', '0004_auto_20210418_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='bio',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='dob',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date.today)]),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='height_feet',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='height_inches',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(11)]),
        ),
        migrations.AlterField(
            model_name='workout',
            name='calories',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(10000)]),
        ),
        migrations.AlterField(
            model_name='workout',
            name='date',
            field=models.DateField(null=True, validators=[django.core.validators.MaxValueValidator(datetime.date.today)]),
        ),
        migrations.AlterField(
            model_name='workout',
            name='distance',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='workout',
            name='length',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(1440)]),
        ),
        migrations.AlterField(
            model_name='workout',
            name='notes',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='reps',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='workout',
            name='sets',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='workout',
            name='weight',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
    ]
