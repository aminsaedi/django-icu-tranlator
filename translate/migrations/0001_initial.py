# Generated by Django 4.2.3 on 2023-07-31 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationStrings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('formatjs_id', models.CharField(max_length=100, unique=True)),
                ('default_message', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApplicationStringsTranslations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('string', models.CharField(max_length=255)),
                ('is_approved', models.BooleanField(default=False)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='translate.language')),
                ('translation_string', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='translate.applicationstrings')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
