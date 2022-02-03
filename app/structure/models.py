import os
from uuid import uuid4

from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.postgres.fields import ArrayField
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


def default_task_media():
    return {
        # - картинки вариантов ответа для заданий sent_image предложений'
        "sent_images_id": [],
        # картинка правильного варианта ответа
        "sent_images_id_right": [],
        "sent_video_id": [],
        "sent_audio_A_id": [],
        # аудио второй реплики(для диалогов)
        "sent_audio_B_id": []
    }


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

        ('22', 'draw_character')
    ]

    task_type = models.CharField(max_length=2, choices=TASK_TYPES)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    word = models.ForeignKey(Word, on_delete=models.CASCADE, null=True)
    grammar = models.ForeignKey(Grammar, on_delete=models.CASCADE, null=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)

    # elements
    # слова, у которых при прохождении этого задания срабатывает счетчик "правильно"
    words_active_or_to_del = ArrayField(models.IntegerField(), null=True)
    # слова, которые должны отображаться при показе задания пользователю
    words_to_display = ArrayField(models.IntegerField(), null=True)
    # неправильные слова
    words_wrong = ArrayField(models.IntegerField(), null=True)
    # неправильные грамматики
    grammars_wrong = ArrayField(models.IntegerField(), null=True)

    # right_sentences
    # предлоежние на китайском
    sent_char_A = models.CharField(max_length=120, null=True)
    # предложение на pinyin
    sent_pinyin_A = models.CharField(max_length=120, null=True)
    # 'или предложение на русском(которое используется для выбора среди правильных / неправильных или это список элементов пазла которые используются для выбора среди правильных/неправильных элементов пазла и потом будут отображаться во всплывающем окне правильного ответа. Например sent_lang_A": [{"я": 1}, {"-": 0}, {"Чжан Вэй": 1}, {".": 0}] будет означать, что пользователь будет собирать предложение из пазлов "я" и "Чжан Вэй" и еще других неправильных, а во всплывающем окне правильного ответа будет отображаться польностью "Я - Чжан Вэй."
    sent_lang_A = models.CharField(max_length=120, null=True)
    # предолжение на русском дословно
    sent_lit_A = models.CharField(max_length=120, null=True)
    # все то же самое, используются в случае если задания с диалогами (это вторые реплики)')
    sent_char_B = models.CharField(max_length=120, null=True)
    sent_pinyin_B = models.CharField(max_length=120, null=True)
    sent_lang_B = models.CharField(max_length=120, null=True)
    sent_lit_B = models.CharField(max_length=120, null=True)

    # 'смысл как в right_sentences, только это списки с неправильными вариантами предложений
    sent_char_W = ArrayField(models.CharField(max_length=120), null=True)
    sent_pinyin_W = ArrayField(models.CharField(max_length=120), null=True)
    sent_lang_W = ArrayField(models.CharField(max_length=120), null=True)

    # списки с media_id файлов'
    media = models.JSONField(default=default_task_media, null=True)

    video = models.FileField(upload_to='media/video', null=True)

    def __str__(self):
        return f'{self.task_type}_{self.get_task_type_display()}_id_{self.pk}'
