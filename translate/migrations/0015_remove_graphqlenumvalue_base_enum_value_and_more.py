# Generated by Django 4.2.3 on 2023-08-01 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0014_rename_value_graphqlenumvalue_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graphqlenumvalue',
            name='base_enum_value',
        ),
        migrations.RemoveField(
            model_name='graphqlenumvalue',
            name='enum',
        ),
        migrations.RemoveField(
            model_name='graphqlenumvalue',
            name='is_duplicate',
        ),
        migrations.CreateModel(
            name='GraphqlEnumValueAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('enum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='translate.graphqlenum')),
                ('enum_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='translate.graphqlenumvalue')),
            ],
            options={
                'unique_together': {('enum_value', 'enum')},
            },
        ),
    ]
