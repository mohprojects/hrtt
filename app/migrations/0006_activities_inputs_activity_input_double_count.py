# Generated by Django 4.1.7 on 2024-04-19 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_activities_inputs_activity_input_expenses'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities_inputs',
            name='activity_input_double_count',
            field=models.IntegerField(default=0, verbose_name='Double Count'),
        ),
    ]
