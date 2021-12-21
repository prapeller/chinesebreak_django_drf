from django.db import models

from structure.lang.models import Lang
from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=64)
    is_published = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.name}'
