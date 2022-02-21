import mimetypes
import os
from uuid import uuid4

import requests
from django.contrib.postgres.fields import ArrayField
from django.core.files import File
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.temp import NamedTemporaryFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.deconstruct import deconstructible

from elements.models import Word, Grammar, Character
from users.models import User


@deconstructible
class PathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = f'{instance.pk}_{instance}.{ext}'
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)


class Lang(models.Model):
    name = models.CharField(max_length=64)
    is_published = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}_id_{self.pk}'


class Course(models.Model):
    name = models.CharField(max_length=64)
    is_published = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}_id_{self.pk}'


class Topic(models.Model):
    name = models.CharField(max_length=64)
    image = models.FileField(upload_to=PathAndRename('images/topics/'),
                             null=True, blank=True,
                             validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png'])])
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}_id_{self.pk}'


class Lesson(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return f'lesson_to_{self.topic.name}_id_{self.pk}'

    # списки с media_id файлов'


def default_task_media():
    return {
        # картинки вариантов ответа для заданий sent_image предложений':[[id, 0], [id, 1]]: 1/0 -> правильно/неправильно
        "sent_images_id": [[], []],
        # видео
        "video_id": [],
        # аудио реплик
        "sent_audio_A_id": [],
        "sent_audio_B_id": []
    }


def default_1d_array():
    return []


def default_2d_array():
    return [[], ]


class Task(models.Model):
    TASK_TYPES = [
        ('1', 'word_image'),
        ('2', 'word_char_from_lang'),
        ('3', 'word_lang_from_char'),
        ('4', 'word_char_from_video'),
        ('5', 'word_match'),

        ('6', 'sent_image'),
        ('7', 'sent_char_from_lang'),
        ('8', 'sent_lang_from_char'),
        ('9', 'sent_lang_from_video'),
        ('10', 'sent_say_from_char'),
        ('11', 'sent_say_from_video'),
        ('12', 'sent_paste_from_char'),
        ('13', 'sent_choose_from_char'),
        ('14', 'sent_delete_from_char'),

        ('15', 'dialog_A_char_from_char'),
        ('16', 'dialog_B_char_from_video'),
        ('17', 'dialog_A_puzzle_char_from_char'),
        ('18', 'dialog_B_puzzle_char_from_char'),

        ('19', 'puzzle_char_from_lang'),
        ('20', 'puzzle_lang_from_char'),
        ('21', 'puzzle_char_from_video'),

        ('22', 'word_write_from_video'),
        ('23', 'grammar_choose_from_video'),
        ('24', 'draw_character')
    ]

    task_type = models.CharField(max_length=2, choices=TASK_TYPES)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)

    # связанное слово
    word = models.ForeignKey(Word, on_delete=models.SET_NULL, null=True)
    # используемые слова [[id, 1, 1], [id, 0, 0]]: 1/0 -> активно/неактивно, 1/0 -> показывается/не показывается
    words = ArrayField(ArrayField(models.IntegerField(), null=True), null=True, default=default_2d_array)
    # неправильные слова
    words_wrong = ArrayField(models.IntegerField(), null=True, default=default_1d_array)

    # связанная грамматика
    grammar = models.ForeignKey(Grammar, on_delete=models.SET_NULL, null=True)
    # используемые в предложениях грамматики [[id, 1], [id, 0]]: 1/0 -> активно/неактивно
    grammars = ArrayField(ArrayField(models.IntegerField(), null=True), null=True, default=default_2d_array)
    # неправильные грамматики
    grammars_wrong = ArrayField(models.IntegerField(), null=True, default=default_1d_array)

    # связанный иероглиф
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)

    # right_sentences
    # sent_char, sent_pinyin, sent_lang, sent_lit, sent_audio - предлоежния (_A - первые реплики, _B - вторые)
    sent_char_A = models.CharField(max_length=120, null=True)
    sent_pinyin_A = models.CharField(max_length=120, null=True)
    sent_lang_A = models.CharField(max_length=120, null=True)
    sent_lit_A = models.CharField(max_length=120, null=True)

    sent_audio_A = models.FileField(upload_to=PathAndRename('audio/tasks/'),
                                    null=True, blank=True,
                                    validators=[FileExtensionValidator(['mp3', 'wav'])])

    sent_char_B = models.CharField(max_length=120, null=True)
    sent_pinyin_B = models.CharField(max_length=120, null=True)
    sent_lang_B = models.CharField(max_length=120, null=True)
    sent_lit_B = models.CharField(max_length=120, null=True)

    sent_audio_B = models.FileField(upload_to=PathAndRename('audio/tasks/'),
                                    null=True, blank=True,
                                    validators=[FileExtensionValidator(['mp3', 'wav'])])

    # [[sent_wrong_pinyin, sent_wrong_char, sent_wrong_lang], [ ... ], ]
    sent_wrong = ArrayField(ArrayField(models.CharField(max_length=120, null=True, blank=True)), null=True, default=default_2d_array)

    # варианты картинок для предложений (первое правильное)
    sent_images = ArrayField(models.FileField(upload_to=PathAndRename('images/tasks/'),
                                              validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png'])]),
                             null=True, blank=True, default=default_1d_array
                             )

    video = models.FileField(upload_to=PathAndRename('video/tasks/'),
                             null=True, blank=True,
                             validators=[FileExtensionValidator(['mp4'])])

    def __str__(self):
        return f'{self.task_type}_{self.get_task_type_display()}_id_{self.pk}'

    def add_sent_wrong(self, sent_wrong_pinyin, sent_wrong_char):
        if sent_wrong_pinyin and sent_wrong_char:
            self.sent_wrong.append([sent_wrong_pinyin, sent_wrong_char])
            self.save()

    def get_task_words(self):
        return [(idx, Word.objects.get(id=word[0]), word[1], word[2], word[3], word[4]) for idx, word in
                enumerate(self.words)]

    def get_right_sent_from_task_words(self):
        words_qs = [Word.objects.get(id=word[0]) for word in self.words]
        pinyin_list = ' '.join([word.pinyin for word in words_qs]).rstrip()
        char_list = ''.join([word.char for word in words_qs])
        return (pinyin_list, char_list)

    def save_task_sent(self,
                       sent_char_A=None,
                       sent_pinyin_A=None,
                       sent_lang_A=None,
                       sent_lit_A=None,
                       sent_char_B=None,
                       sent_pinyin_B=None,
                       sent_lang_B=None,
                       sent_lit_B=None):
        self.sent_char_A = sent_char_A
        self.sent_pinyin_A = sent_pinyin_A
        self.sent_lit_A = sent_lit_A
        self.sent_lang_A = sent_lang_A
        self.sent_char_B = sent_char_B
        self.sent_pinyin_B = sent_pinyin_B
        self.sent_lang_B = sent_lang_B
        self.sent_lit_B = sent_lit_B
        self.save()

    def save_task_video(self,
                        video_file=None,
                        video_url=None):
        if video_file:
            ext = video_file.name.split('.')[-1]
            self.video.save(name=f'{ext}', content=File(video_file), save=True)

        if video_url and not video_file:
            resp = requests.get(video_url)
            ext = mimetypes.guess_extension(resp.headers['content-type'])

            temp_file = NamedTemporaryFile(delete=True)
            temp_file.write(resp.content)
            temp_file.flush()

            self.video.save(name=f'{ext}', content=File(temp_file), save=True)

    def save_task_audio(self,
                        sent_audio_A_file=None,
                        sent_audio_A_url=None,
                        sent_audio_B_file=None,
                        sent_audio_B_url=None):
        if sent_audio_A_file:
            ext = sent_audio_A_file.name.split('.')[-1]
            self.video.save(name=f'{ext}', content=File(sent_audio_A_file), save=True)

        if sent_audio_A_url and not sent_audio_A_file:
            resp = requests.get(sent_audio_A_url)
            ext = mimetypes.guess_extension(resp.headers['content-type'])

            temp_file = NamedTemporaryFile(delete=True)
            temp_file.write(resp.content)
            temp_file.flush()

            self.sent_audio_A.save(name=f'{ext}', content=File(temp_file), save=True)

        if sent_audio_B_file:
            ext = sent_audio_B_file.name.split('.')[-1]
            self.video.save(name=f'{ext}', content=File(sent_audio_B_file), save=True)

        if sent_audio_B_url and not sent_audio_B_file:
            resp = requests.get(sent_audio_B_url)
            ext = mimetypes.guess_extension(resp.headers['content-type'])

            temp_file = NamedTemporaryFile(delete=True)
            temp_file.write(resp.content)
            temp_file.flush()

            self.sent_audio_B.save(name=f'{ext}', content=File(temp_file), save=True)

    def save_task_image(self,
                        image_file=None,
                        image_url=None):
        if image_file:
            path = default_storage.save(settings.BASE_DIR / f'static/media/images/tasks/{image_file.name}', image_file.file)
            self.sent_images.append(f'/media/{path}')

        if image_url and not image_file:
            resp = requests.get(image_url)
            ext = mimetypes.guess_extension(resp.headers['content-type'])

            temp_file = NamedTemporaryFile(delete=True)
            temp_file.write(resp.content)
            temp_file.flush()
            file = File(temp_file)

            path = default_storage.save(settings.BASE_DIR / f'static/media/images/tasks/{file.name.replace("/tmp/", "")}{ext}', file.file)
            self.sent_images.append(f'/media/{path}')
            self.save()
