# Generated by Django 4.0.2 on 2022-02-20 19:40

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import structure.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_published', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('image', models.FileField(blank=True, null=True, upload_to=structure.models.PathAndRename('images/topics/'), validators=[django.core.validators.FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png'])])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.course')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.CharField(choices=[('1', 'word_image'), ('2', 'word_char_from_lang'), ('3', 'word_lang_from_char'), ('4', 'word_char_from_video'), ('5', 'word_match'), ('6', 'sent_image'), ('7', 'sent_char_from_lang'), ('8', 'sent_lang_from_char'), ('9', 'sent_lang_from_video'), ('10', 'sent_say_from_char'), ('11', 'sent_say_from_video'), ('12', 'sent_paste_from_char'), ('13', 'sent_choose_from_char'), ('14', 'sent_delete_from_char'), ('15', 'dialog_A_char_from_char'), ('16', 'dialog_B_char_from_video'), ('17', 'dialog_A_puzzle_char_from_char'), ('18', 'dialog_B_puzzle_char_from_char'), ('19', 'puzzle_char_from_lang'), ('20', 'puzzle_lang_from_char'), ('21', 'puzzle_char_from_video'), ('22', 'word_write_from_video'), ('23', 'grammar_choose_from_video'), ('24', 'draw_character')], max_length=2)),
                ('words', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None), default=structure.models.default_2d_array, null=True, size=None)),
                ('words_wrong', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=structure.models.default_1d_array, null=True, size=None)),
                ('grammars', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None), default=structure.models.default_2d_array, null=True, size=None)),
                ('grammars_wrong', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=structure.models.default_1d_array, null=True, size=None)),
                ('sent_char_A', models.CharField(max_length=120, null=True)),
                ('sent_pinyin_A', models.CharField(max_length=120, null=True)),
                ('sent_lang_A', models.CharField(max_length=120, null=True)),
                ('sent_lit_A', models.CharField(max_length=120, null=True)),
                ('sent_audio_A', models.FileField(blank=True, null=True, upload_to=structure.models.PathAndRename('audio/tasks/'), validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav'])])),
                ('sent_char_B', models.CharField(max_length=120, null=True)),
                ('sent_pinyin_B', models.CharField(max_length=120, null=True)),
                ('sent_lang_B', models.CharField(max_length=120, null=True)),
                ('sent_lit_B', models.CharField(max_length=120, null=True)),
                ('sent_audio_B', models.FileField(blank=True, null=True, upload_to=structure.models.PathAndRename('audio/tasks/'), validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav'])])),
                ('sent_wrong', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=120, null=True), size=None), default=structure.models.default_2d_array, null=True, size=None)),
                ('sent_images', django.contrib.postgres.fields.ArrayField(base_field=models.FileField(upload_to=structure.models.PathAndRename('images/tasks/'), validators=[django.core.validators.FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png'])]), blank=True, default=structure.models.default_1d_array, null=True, size=None)),
                ('video', models.FileField(blank=True, null=True, upload_to=structure.models.PathAndRename('video/tasks/'), validators=[django.core.validators.FileExtensionValidator(['mp4'])])),
                ('character', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elements.character')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('grammar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='elements.grammar')),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='structure.lesson')),
                ('word', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='elements.word')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.topic'),
        ),
        migrations.CreateModel(
            name='Lang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_published', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='lang',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.lang'),
        ),
    ]
