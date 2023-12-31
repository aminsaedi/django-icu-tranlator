# Generated by Django 4.2.3 on 2023-07-31 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0005_autotranslationlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autotranslationlog',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='autotranslationlog',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='autotranslationlog',
            name='total_translated',
            field=models.IntegerField(default=0),
        ),
    ]
