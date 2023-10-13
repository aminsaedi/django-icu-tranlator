# Generated by Django 4.2.3 on 2023-08-09 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0026_alter_customkeytranslation_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuplicateString',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('default_message', models.TextField()),
                ('count', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='customkey',
            options={'verbose_name': 'custom key translation', 'verbose_name_plural': '3. Custom Key Translations'},
        ),
        migrations.AlterModelOptions(
            name='customkeytranslation',
            options={},
        ),
    ]