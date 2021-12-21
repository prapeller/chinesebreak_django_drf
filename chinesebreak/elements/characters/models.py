from django.db import models

class Character(models.Model):
    char = models.CharField(max_length=64)
    pinyin = models.CharField(max_length=64)
    lang = models.CharField(max_length=64)
    image = models.ImageField()
    audio = models.FileField()
    video = models.FileField()

    def __str__(self):
        return f'{self.id} | char: {self.char}, pinyin: {self.pinyin}, lang: {self.lang}'