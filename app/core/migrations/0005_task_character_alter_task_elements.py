# Generated by Django 4.0 on 2021-12-09 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_character_grammar_word_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='character',
            field=models.ForeignKey(default='x', on_delete=django.db.models.deletion.CASCADE, to='core.character'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='elements',
            field=models.JSONField(default={'grammars_id_wrong': [], 'words_id_active_or_to_del': [], 'words_id_to_display': [], 'words_id_wrong': []}),
        ),
    ]
