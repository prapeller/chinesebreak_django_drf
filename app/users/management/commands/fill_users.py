from django.core.management.base import BaseCommand
from django.db import connections
from django.contrib.auth import get_user_model

from core.models import User


class Command(BaseCommand):
    """Command to fill empty db with 1 admin (username: admin, password: admin)
    and 9 users"""

    def handle(self, *args, **options):
        self.stdout.write('creating users...')
        for i in range(10):
            if i == 0:
                user = get_user_model().objects.create_superuser(
                    email='admin@admin.com', password='admin', username='admin',
                    first_name=f'first{i}', last_name=f'last{i}',
                )

            else:
                user = get_user_model().objects.create_user(
                    email=f'user@user{i}.com', password=f'user{i}', username=f'user{i}',
                    first_name=f'first{i}', last_name=f'last{i}',
                )
            self.stdout.write(f'user {user.username} created')
