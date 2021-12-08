from django.core.management.base import BaseCommand
from django.db import connection

from core.models import User


class Command(BaseCommand):
    """delete all users from db and reset sequences"""

    def handle(self, *args, **options):
        users = User.objects.all()
        users.delete()

        with connection.cursor() as c:
            c.execute("""
            SELECT setval(pg_get_serial_sequence('"core_user_groups"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "core_user_groups";
            SELECT setval(pg_get_serial_sequence('"core_user_user_permissions"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "core_user_user_permissions";
            SELECT setval(pg_get_serial_sequence('"core_user"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "core_user";
            """
                      )
