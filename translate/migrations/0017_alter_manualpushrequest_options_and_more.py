# Generated by Django 4.2.3 on 2023-08-01 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0016_graphqlenum_values_delete_graphqlenumvalueassignment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manualpushrequest',
            options={'verbose_name': 'Force sync strings', 'verbose_name_plural': 'Force sync strings'},
        ),
        migrations.AddField(
            model_name='autotranslationlog',
            name='target_type',
            field=models.CharField(choices=[('application_string', 'Application String'), ('graphql_enum_value', 'Graphql Enum Value')], default='application_string', max_length=100),
        ),
    ]
