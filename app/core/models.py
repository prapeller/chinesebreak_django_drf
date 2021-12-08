from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, \
    AbstractUser


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a new superuser"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    """Custom user model with unique username and email"""
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=64, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']

class Lang(models.Model):
    name = models.CharField(max_length=64)
    is_published = models.BooleanField(default=False)
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

    # courses

    def __str__(self):
        return f'{self.id} | {self.name}'


class Course(models.Model):
    name = models.CharField(max_length=64)
    is_published = models.BooleanField(default=False)
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('Lang', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.name}'


class Topic(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField()
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.name}'


class Lesson(models.Model):
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.topic}'


# class Task(models.Model):
#     elements = models.JSONField(default={
#         "words_id": [],
#         "grammar_id": [],
#         "character_id": [],
#         # слова, у которых при прохождении этого задания срабатывает счетчик "правильно"
#         "words_id_active_or_to_del": [],
#         # слова, которые должны отображаться при показе задания пользователю
#         "words_id_to_display": [],
#         # неправильные слова
#         "words_id_wrong": [],
#         "grammars_id_wrong": []
#     })
#     right_sentences = models.JSONField(default={
#         # предлоежние на китайском
#         "sent_char_A": [],
#         # предложение на pinyin
#         "sent_pinyin_A": [],
#         # 'или предложение на русском(которое используется для выбора среди правильных / неправильных или это список элементов пазла которые используются для выбора среди правильных/неправильных элементов пазла и потом будут отображаться во всплывающем окне правильного ответа. Например sent_lang_A": [{"я": 1}, {"-": 0}, {"Чжан Вэй": 1}, {".": 0}] будет означать, что пользователь будет собирать предложение из пазлов "я" и "Чжан Вэй" и еще других неправильных, а во всплывающем окне правильного ответа будет отображаться польностью "Я - Чжан Вэй."
#         "sent_lang_A": [],
#         # предолжение на русском дословно
#         "sent_lit_A": [],
#         # все то же самое, используются в случае если задания с диалогами (это вторые реплики)')
#         "sent_char_B": [],
#         "sent_pinyin_B": [],
#         "sent_lang_B": [],
#         "sent_lit_B": []
#     })
#     # 'смысл как в right_sentences, только это списки с неправильными вариантами предложений
#     wrong_sentences = models.JSONField(default={
#         "sent_char": [],
#         "sent_pinyin": [],
#         "sent_lang": []
#     })
#     # списки с media_id файлов'
#     media = models.JSONField(default={
#         # - картинки вариантов ответа для заданий sent_image предложений'
#         "sent_images_id": [],
#         # картинка правильного варианта ответа
#         "sent_images_id_right": [],
#         "sent_video_id": [],
#         "sent_audio_A_id": [],
#         # аудио второй реплики(для диалогов)
#         "sent_audio_B_id": []
#     })
#
#     TASK_TYPES = [
#         (1, 'word_image'),
#         (2, 'word_char_from_lang'),
#         (3, 'word_lang_from_char'),
#         (4, 'word_char_from_video'),
#         (5, 'word_match'),
#         (6, 'sent_image'),
#         (7, 'sent_char_from_lang'),
#         (8, 'sent_lang_from_char'),
#         (9, 'sent_lang_from_video'),
#         (10, 'sent_say_from_char'),
#         (11, 'sent_say_from_video'),
#         (12, 'sent_paste_from_char'),
#         (13, 'sent_choose_from_char'),
#         (14, 'sent_delete_from_char'),
#         (15, 'dialog_A_char_from_char'),
#         (16, 'dialog_B_char_from_video'),
#         (17, 'dialog_A_puzzle_char_from_char'),
#         (18, 'dialog_B_puzzle_char_from_char'),
#         (19, 'puzzle_char_from_lang'),
#         (20, 'puzzle_lang_from_char'),
#         (21, 'puzzle_char_from_video'),
#         (22, 'draw_character')
#     ]
#
#     task_type = models.CharField(max_length=2, choices=TASK_TYPES)
#     creator = models.ForeignKey('User', on_delete=models.SET_NULL)
#     lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
#     word = models.ForeignKey('Word', on_delete=models.CASCADE)
#     grammar = models.ForeignKey('Grammar', on_delete=models.CASCADE)
#     video = models.ForeignKey('Media', on_delete=models.CASCADE)
#
#
#     def __str__(self):
#         return f'{self.id} | {self.task_type}'


# class Media(models.Model):
#     name = models.CharField(max_length=64)
#     type = models.Choices(('mp4', 'mp3', 'png', 'jpg', 'gif', 'pdf', 'svg'))
#     file_path = db.Column(db.String(2083))
#     topic_image_fk = db.Column(db.ForeignKey('topics.id', ondelete='CASCADE', onupdate='CASCADE'),
#                                index=True)
#     word_image_fk = db.Column(db.ForeignKey('words.id', ondelete='CASCADE', onupdate='CASCADE'),
#                               index=True)
#     word_audio_fk = db.Column(db.ForeignKey('words.id', ondelete='CASCADE', onupdate='CASCADE'),
#                               index=True)
#     word_video_fk = db.Column(db.ForeignKey('words.id', ondelete='CASCADE', onupdate='CASCADE'),
#                               index=True)
#     task_video_fk = db.Column(db.ForeignKey("tasks.id", ondelete='CASCADE', onupdate='CASCADE'),
#                               index=True)
#     task_image_fk = db.Column(db.ForeignKey("tasks.id", ondelete='CASCADE', onupdate='CASCADE'), index=True)
#
#
# class Word(models.Model):
#     char = db.Column(db.String(50), index=True)
#     pinyin = db.Column(db.String(50), index=True)
#     lang = db.Column(db.String(50), index=True)
#     lit = db.Column(db.String(50), index=True)
#
#     image_id = db.Column(db.ForeignKey('media.id'))
#     audio_id = db.Column(db.ForeignKey('media.id'))
#     video_id = db.Column(db.ForeignKey('media.id'))
#
#     images = db.relationship('Media', foreign_keys=[image_id], cascade='all, delete')
#     audios = db.relationship('Media', foreign_keys=[audio_id], cascade='all, delete')
#     videos = db.relationship('Media', foreign_keys=[video_id], cascade='all, delete')
#     tasks = db.relationship('Task', backref='word')
#
#     def __repr__(self):
#         return f'id: {self.id}, char: {self.char}, pinyin: {self.pinyin}, lang: {self.lang}, lit: {self.lit}'
#
#
# class Grammar(models.Model):
#     name = db.Column(db.String(512), index=True)
#     explanation = db.Column(db.Text, index=True)
#     char = db.Column(db.String(512), index=True)
#     pinyin = db.Column(db.String(512), index=True)
#     lang = db.Column(db.String(512), index=True)
#     lit = db.Column(db.String(512), index=True)
#     structure = db.Column(db.String(512), index=True)
#
#     tasks = db.relationship('Task', backref='grammar')
#
#     def __repr__(self):
#         return f'id: {self.id}, name: {self.name}'
#
# class Character(models.Model):
#     char = db.Column(db.String(50), nullable=False, index=True)
#     pinyin = db.Column(db.String(50), nullable=False, index=True)
#     lang = db.Column(db.String(50), nullable=False, index=True)
#     image_media_id = db.Column(db.ForeignKey('media.id'), index=True)
#     audio_media_id = db.Column(db.ForeignKey('media.id'), index=True)
#     char_anim = db.Column(db.JSON, nullable=False)
#
#     audio_media = db.relationship('Media', primaryjoin='Character.audio_media_id == Media.id')
#     image_media = db.relationship('Media', primaryjoin='Character.image_media_id == Media.id')
#     topic = db.relationship('Topic')
