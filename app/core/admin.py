from django.contrib import admin

from core.models import User, Course, Topic, Lesson, Lang

admin.site.register(User)
admin.site.register(Lang)
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Lesson)