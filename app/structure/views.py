from rest_framework.viewsets import ModelViewSet

from structure.models import Lang, Course, Topic, Lesson, Task


class LangModelViewSet(ModelViewSet):
    queryset = Lang.objects.all()


class CourseModelViewSet(ModelViewSet):
    queryset = Course.objects.all()


class TopicModelViewSet(ModelViewSet):
    queryset = Topic.objects.all()


class LessonModelViewSet(ModelViewSet):
    queryset = Lesson.objects.all()


class TaskModelViewSet(ModelViewSet):
    queryset = Task.objects.all()
