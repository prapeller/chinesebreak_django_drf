# Generated by Django 4.0 on 2021-12-09 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_language_course_lang'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char', models.CharField(max_length=64)),
                ('pinyin', models.CharField(max_length=64)),
                ('lang', models.CharField(max_length=64)),
                ('image', models.ImageField(upload_to='')),
                ('audio', models.FileField(upload_to='')),
                ('video', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Grammar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('explanation', models.CharField(max_length=512)),
                ('char', models.CharField(max_length=512)),
                ('pinyin', models.CharField(max_length=512)),
                ('lang', models.CharField(max_length=512)),
                ('lit', models.CharField(max_length=512)),
                ('structure', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char', models.CharField(max_length=64)),
                ('pinyin', models.CharField(max_length=64)),
                ('lang', models.CharField(max_length=64)),
                ('lit', models.CharField(max_length=64)),
                ('image', models.ImageField(upload_to='')),
                ('audio', models.FileField(upload_to='')),
                ('video', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elements', models.JSONField(default={'character_id': [], 'grammar_id': [], 'grammars_id_wrong': [], 'words_id': [], 'words_id_active_or_to_del': [], 'words_id_to_display': [], 'words_id_wrong': []})),
                ('right_sentences', models.JSONField(default={'sent_char_A': [], 'sent_char_B': [], 'sent_lang_A': [], 'sent_lang_B': [], 'sent_lit_A': [], 'sent_lit_B': [], 'sent_pinyin_A': [], 'sent_pinyin_B': []})),
                ('wrong_sentences', models.JSONField(default={'sent_char': [], 'sent_lang': [], 'sent_pinyin': []})),
                ('media', models.JSONField(default={'sent_audio_A_id': [], 'sent_audio_B_id': [], 'sent_images_id': [], 'sent_images_id_right': [], 'sent_video_id': []})),
                ('task_type', models.CharField(choices=[('1', 'word_image'), ('2', 'word_char_from_lang'), ('3', 'word_lang_from_char'), ('4', 'word_char_from_video'), ('5', 'word_match'), ('6', 'sent_image'), ('7', 'sent_char_from_lang'), ('8', 'sent_lang_from_char'), ('9', 'sent_lang_from_video'), ('10', 'sent_say_from_char'), ('11', 'sent_say_from_video'), ('12', 'sent_paste_from_char'), ('13', 'sent_choose_from_char'), ('14', 'sent_delete_from_char'), ('15', 'dialog_A_char_from_char'), ('16', 'dialog_B_char_from_video'), ('17', 'dialog_A_puzzle_char_from_char'), ('18', 'dialog_B_puzzle_char_from_char'), ('19', 'puzzle_char_from_lang'), ('20', 'puzzle_lang_from_char'), ('21', 'puzzle_char_from_video'), ('22', 'draw_character')], max_length=2)),
                ('video', models.FileField(upload_to='')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.user')),
                ('grammar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.grammar')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.lesson')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.word')),
            ],
        ),
    ]
