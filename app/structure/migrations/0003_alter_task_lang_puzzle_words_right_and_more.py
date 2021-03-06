# Generated by Django 4.0.2 on 2022-02-24 18:31

import django.contrib.postgres.fields
from django.db import migrations, models
import structure.models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0002_task_grammars_wrong'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='lang_puzzle_words_right',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=120, null=True), default=structure.models.default_1d_array, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='task',
            name='lang_puzzle_words_wrong',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=120, null=True), default=structure.models.default_1d_array, null=True, size=None),
        ),
    ]
