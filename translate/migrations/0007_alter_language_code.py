# Generated by Django 4.2.3 on 2023-08-01 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0006_alter_autotranslationlog_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='code',
            field=models.CharField(choices=[('en-US', 'English'), ('fr-CA', 'French (Canada)'), ('fa-IR', 'Persian (Iran)'), ('he-IL', 'Hebrew')], max_length=5, unique=True),
        ),
    ]
