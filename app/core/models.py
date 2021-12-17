from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, \
    AbstractUser
from django import forms
from django.contrib.postgres.fields import ArrayField

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

    def __str__(self):
        return f'{self.id} | {self.username}'


class Lang(models.Model):
    name = models.CharField(max_length=64)
    is_published = models.BooleanField(default=False)
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.id} | {self.name}'


class LangForm(forms.ModelForm):
    class Meta:
        model = Lang
        fields = '__all__'


class Course(models.Model):
    name = models.CharField(max_length=64)
    is_published = models.BooleanField(default=False)
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    lang = models.ForeignKey('Lang', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.name}'


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class Topic(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField()
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.name}'


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'


class Lesson(models.Model):
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.topic}'


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'


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

    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    grammar = models.ForeignKey('Grammar', on_delete=models.CASCADE)
    character = models.ForeignKey('Character', on_delete=models.CASCADE)

    # elements

        # слова, у которых при прохождении этого задания срабатывает счетчик "правильно"
    words_active_or_to_del = ArrayField(models.IntegerField())
        # слова, которые должны отображаться при показе задания пользователю
    words_to_display = ArrayField(models.IntegerField())
        # неправильные слова
    words_wrong = ArrayField(models.IntegerField())
    grammars_wrong = ArrayField(models.IntegerField())

    # right_sentences

        # предлоежние на китайском
    sent_char_A = models.CharField(max_length=120)
        # предложение на pinyin
    sent_pinyin_A = models.CharField(max_length=120)
        # 'или предложение на русском(которое используется для выбора среди правильных / неправильных или это список элементов пазла которые используются для выбора среди правильных/неправильных элементов пазла и потом будут отображаться во всплывающем окне правильного ответа. Например sent_lang_A": [{"я": 1}, {"-": 0}, {"Чжан Вэй": 1}, {".": 0}] будет означать, что пользователь будет собирать предложение из пазлов "я" и "Чжан Вэй" и еще других неправильных, а во всплывающем окне правильного ответа будет отображаться польностью "Я - Чжан Вэй."
    sent_lang_A = models.CharField(max_length=120)
        # предолжение на русском дословно
    sent_lit_A = models.CharField(max_length=120)
        # все то же самое, используются в случае если задания с диалогами (это вторые реплики)')
    sent_char_B = models.CharField(max_length=120)
    sent_pinyin_B = models.CharField(max_length=120)
    sent_lang_B = models.CharField(max_length=120)
    sent_lit_B = models.CharField(max_length=120)

    # 'смысл как в right_sentences, только это списки с неправильными вариантами предложений
    sent_char_W = ArrayField(models.CharField(max_length=120))
    sent_pinyin_W = ArrayField(models.CharField(max_length=120))
    sent_lang_W = ArrayField(models.CharField(max_length=120))

    def default_media(self):
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
    # списки с media_id файлов'
    media = models.JSONField(default=default_media)

    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    video = models.FileField()

    def __str__(self):
        return f'{self.id} | {self.task_type}'


class Word(models.Model):
    char = models.CharField(max_length=64)
    pinyin = models.CharField(max_length=64)
    lang = models.CharField(max_length=64)
    lit = models.CharField(max_length=64)

    image = models.ImageField()
    audio = models.FileField()
    video = models.FileField()

    def __str__(self):
        return f'{self.id} | char: {self.char}, pinyin: {self.pinyin}, lang: {self.lang}, lit: {self.lit}'


class Grammar(models.Model):
    name = models.CharField(max_length=512)
    explanation = models.CharField(max_length=512)
    char = models.CharField(max_length=512)
    pinyin = models.CharField(max_length=512)
    lang = models.CharField(max_length=512)
    lit = models.CharField(max_length=512)
    structure = models.CharField(max_length=512)

    def __str__(self):
        return f'{self.id} | {self.name}'


class Character(models.Model):
    char = models.CharField(max_length=64)
    pinyin = models.CharField(max_length=64)
    lang = models.CharField(max_length=64)
    image = models.ImageField()
    audio = models.FileField()
    video = models.FileField()

    def __str__(self):
        return f'{self.id} | char: {self.char}, pinyin: {self.pinyin}, lang: {self.lang}'
