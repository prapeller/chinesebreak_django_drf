# Generated by Django 4.0 on 2022-02-01 14:59

import django.core.validators
from django.db import migrations, models
import structure.models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0009_alter_topic_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=structure.models.PathAndRename('images/topics/'), validators=[django.core.validators.FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png'])]),
        ),
    ]
