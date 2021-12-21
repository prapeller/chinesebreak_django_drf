from django.db import models

class Lesson(models.Model):
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.topic}'
