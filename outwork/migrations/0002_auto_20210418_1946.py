# Generated by Django 3.1.5 on 2021-04-18 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outwork', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='workout',
            name='calories',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
