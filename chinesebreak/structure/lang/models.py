from django.db import models
from users.models import User


class Lang(models.Model):
    name = models.CharField(max_length=64)
    is_published = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.id} | {self.name}'
