# Generated by Django 4.2.3 on 2023-08-02 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0018_manualpushrequest_target_type_alter_language_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManualTranslateRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('is_success', models.BooleanField(default=False)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('target_type', models.CharField(choices=[('application_string', 'Application String'), ('graphql_enum_value', 'Graphql Enum Value')], default='application_string', max_length=100)),
            ],
            options={
                'verbose_name': 'Force translate strings',
                'verbose_name_plural': 'Force translate strings',
            },
        ),
    ]
