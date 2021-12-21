from django.db import models

from structure.course.models import Course
from users.models import User


class Topic(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.name}'
