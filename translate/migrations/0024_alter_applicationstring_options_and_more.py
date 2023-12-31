# Generated by Django 4.2.3 on 2023-08-02 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0023_remove_customkey_default_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicationstring',
            options={'verbose_name': 'application String', 'verbose_name_plural': '1. Application Strings'},
        ),
        migrations.AlterModelOptions(
            name='graphqlenumvalue',
            options={'verbose_name': 'enum item', 'verbose_name_plural': '2. Enum Items'},
        ),
        migrations.AlterField(
            model_name='applicationstring',
            name='default_message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='applicationstring',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='applicationstringstranslation',
            name='string',
            field=models.TextField(blank=True, default=''),
        ),
    ]
