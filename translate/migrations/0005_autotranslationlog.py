# Generated by Django 4.2.3 on 2023-07-31 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0004_applicationstringstranslation_unique_translation_string_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoTranslationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('total_translated', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
