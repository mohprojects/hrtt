# Generated by Django 4.1.7 on 2023-11-30 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='organization_id',
            field=models.IntegerField(default=0, verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='activities_inputs',
            name='organization_id',
            field=models.IntegerField(default=0, verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='activities_inputs',
            name='project_id',
            field=models.IntegerField(default=0, verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='organizations',
            name='organization_status',
            field=models.IntegerField(default=2, verbose_name='Status'),
        ),
    ]