# Generated by Django 4.2.3 on 2023-08-01 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0009_remove_applicationstringstranslation_is_special_char_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoPushLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('is_success', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
