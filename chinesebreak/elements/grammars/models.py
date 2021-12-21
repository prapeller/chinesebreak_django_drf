from django.db import models

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
