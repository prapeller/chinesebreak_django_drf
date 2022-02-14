import mimetypes
import os
from uuid import uuid4
from io import BytesIO
import requests

from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.deconstruct import deconstructible


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


class Character(models.Model):
    char = models.CharField(max_length=64)
    pinyin = models.CharField(max_length=64)
    lang = models.CharField(max_length=64)
    image = models.ImageField()
    audio = models.FileField()
    video = models.FileField()

    def __str__(self):
        return f'{self.id} | char: {self.char}, pinyin: {self.pinyin}, lang: {self.lang}'


class Grammar(models.Model):
    name = models.CharField(max_length=512)
    explanation = models.CharField(max_length=512)
    char = models.CharField(max_length=512)
    pinyin = models.CharField(max_length=512)
    lang = models.CharField(max_length=512)
    lit = models.CharField(max_length=512)
    structure = models.CharField(max_length=512)

    def __str__(self):
        return f'{self.name}'


class Word(models.Model):
    char = models.CharField(max_length=64)
    pinyin = models.CharField(max_length=64)
    lang = models.CharField(max_length=64)
    lit = models.CharField(max_length=64)

    image = models.FileField(upload_to=PathAndRename('images/words/'),
                             null=True, blank=True,
                             validators=[FileExtensionValidator(['svg', 'jpg', 'jpeg', 'png'])])

    audio = models.FileField(upload_to=PathAndRename('audio/words/'),
                             null=True, blank=True,
                             validators=[FileExtensionValidator(['mp3', 'mp4', 'wav'])])

    video = models.FileField(upload_to=PathAndRename('audio/video/'),
                             null=True, blank=True,
                             validators=[FileExtensionValidator(['mp4'])])

    def __str__(self):
        return f'{self.pinyin}_{self.char}_{self.lang}_({self.lit})'

    def save_audio_with_url(self, url):
        resp = requests.get(url)
        ext = mimetypes.guess_extension(resp.headers['content-type'])

        temp_file = NamedTemporaryFile(delete=True)
        temp_file.write(resp.content)
        temp_file.flush()

        self.audio.save(name=f'temp{ext}', content=File(temp_file), save=True)

    def save_image_with_url(self, url):
        resp = requests.get(url)
        ext = mimetypes.guess_extension(resp.headers['content-type'])

        temp_file = NamedTemporaryFile(delete=True)
        temp_file.write(resp.content)
        temp_file.flush()

        self.image.save(name=f'temp{ext}', content=File(temp_file), save=True)

    def save_video_with_url(self, url):
        resp = requests.get(url)
        ext = mimetypes.guess_extension(resp.headers['content-type'])

        temp_file = NamedTemporaryFile(delete=True)
        temp_file.write(resp.content)
        temp_file.flush()

        self.video.save(name=f'temp{ext}', content=File(temp_file), save=True)
