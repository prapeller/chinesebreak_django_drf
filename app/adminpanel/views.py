from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import BaseDeleteView

from adminpanel.forms import TopicForm, LessonForm, TaskForm, CourseForm
from structure.models import Lang, Course, Topic, Lesson, Task


@user_passes_test(lambda u: u is not None and u.is_staff)
def index(request):
    context = {'title': 'Main'}
    return render(request, 'index.html', context)


class LangListView(ListView):
    model = Lang
    extra_context = {'title': 'Lang list'}


class LangCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        self.object = Lang.objects.create(
            name='new',
            creator=self.request.user
        )
        return HttpResponseRedirect(reverse_lazy('adminpanel:lang_update', kwargs={'pk': self.object.pk}))


class LangUpdateView(UpdateView):
    model = Lang
    fields = ['name', 'is_published']
    extra_context = {'title': 'Lang update'}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.extra_context.update({'sub_object_list': Course.objects.filter(lang=self.object)})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse_lazy('adminpanel:lang_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class LangDeleteView(BaseDeleteView):
    model = Lang

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy('adminpanel:lang_list')
        return super().delete(self, request, *args, **kwargs)


class CourseCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        from_url_str = request.META.get('HTTP_REFERER')
        if '/langs/update/' in from_url_str:
            lang_id = int(request.META.get('HTTP_REFERER').split('/')[-2])
            self.object = Course.objects.create(
                name='new',
                lang=Lang.objects.get(id=lang_id),
                creator=request.user
            )
        return HttpResponseRedirect(reverse_lazy('adminpanel:course_update', kwargs={'pk': self.object.pk}))


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    extra_context = {'title': 'Course update'}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.extra_context.update({'sub_object_list': Topic.objects.filter(course=self.object)})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse_lazy('adminpanel:course_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class CourseDeleteView(BaseDeleteView):
    model = Course

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy('adminpanel:lang_update', kwargs={'pk': self.object.lang.pk})
        return super().delete(self, request, *args, **kwargs)


class TopicCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        from_url_str = request.META.get('HTTP_REFERER')
        if '/courses/update/' in from_url_str:
            course_id = int(request.META.get('HTTP_REFERER').split('/')[-2])
            self.object = Topic.objects.create(
                name='new',
                course=Course.objects.get(id=course_id),
                creator=request.user
            )
        return HttpResponseRedirect(reverse_lazy('adminpanel:topic_update', kwargs={'pk': self.object.pk}))


class TopicUpdateView(UpdateView):
    extra_context = {'title': 'Topic update'}
    model = Topic
    form_class = TopicForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.extra_context.update({'sub_object_list': Lesson.objects.filter(topic=self.object)})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse_lazy('adminpanel:topic_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TopicDeleteView(BaseDeleteView):
    model = Topic

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy('adminpanel:course_update', kwargs={'pk': self.object.course.pk})
        return super().delete(self, request, *args, **kwargs)


class LessonCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        from_url_str = request.META.get('HTTP_REFERER')
        if '/topics/update/' in from_url_str:
            topic_id = int(request.META.get('HTTP_REFERER').split('/')[-2])
            self.object = Lesson.objects.create(
                topic=Topic.objects.get(id=topic_id),
                creator=request.user
            )
            self.success_url = reverse_lazy('adminpanel:lesson_update', kwargs={'pk': self.object.pk})
        return HttpResponseRedirect(self.get_success_url())


class LessonUpdateView(UpdateView):
    extra_context = {'title': 'Lesson update',
                     'task_form': TaskForm}
    model = Lesson
    fields = ()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.extra_context.update({'sub_object_list': Task.objects.filter(lesson=self.object)})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task_type = request.POST.get('task_type')
        if task_type:
            new_task = Task.objects.create(
                task_type=task_type,
                creator=request.user,
                lesson=self.get_object()
            )
            if task_type == '1':
                return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_1_update', kwargs={'pk': new_task.pk}))
            if task_type == '2':
                return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_2_update', kwargs={'pk': new_task.pk}))
            if task_type == '3':
                return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_3_update', kwargs={'pk': new_task.pk}))
            if task_type == '4':
                return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_4_update', kwargs={'pk': new_task.pk}))
            if task_type == '5':
                return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_5_update', kwargs={'pk': new_task.pk}))
            if task_type == '6':
                return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_6_update', kwargs={'pk': new_task.pk}))
            if task_type == '7':
                return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_7_update', kwargs={'pk': new_task.pk}))
            if task_type == '8':
                return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_8_update', kwargs={'pk': new_task.pk}))
            if task_type == '9':
                return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_9_update', kwargs={'pk': new_task.pk}))
            if task_type == '10':
                return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_10_update', kwargs={'pk': new_task.pk}))


class LessonDeleteView(DeleteView):
    model = Lesson

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy('adminpanel:topic_update', kwargs={'pk': self.object.topic.pk})
        return super().delete(self, request, *args, **kwargs)


class TaskDeleteView(DeleteView):
    model = Task

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy('adminpanel:lesson_update', kwargs={'pk': self.object.lesson.pk})
        return super().delete(self, request, *args, **kwargs)

class TaskUpdateView(UpdateView):
    extra_context = {'title': 'Task update'}
    model = Task
    fields = ()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_type = self.object.task_type
        if task_type == '1':
            return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_1_update', kwargs={'pk': self.object.pk}))
        if task_type == '2':
            return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_2_update', kwargs={'pk': self.object.pk}))
        if task_type == '3':
            return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_3_update', kwargs={'pk': self.object.pk}))
        if task_type == '4':
            return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_4_update', kwargs={'pk': self.object.pk}))
        if task_type == '5':
            return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_5_update', kwargs={'pk': self.object.pk}))
        if task_type == '6':
            return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_6_update', kwargs={'pk': self.object.pk}))
        if task_type == '7':
            return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_7_update', kwargs={'pk': self.object.pk}))
        if task_type == '8':
            return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_8_update', kwargs={'pk': self.object.pk}))
        if task_type == '9':
            return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_9_update', kwargs={'pk': self.object.pk}))
        if task_type == '10':
            return HttpResponseRedirect(reverse_lazy('adminpanel:task_type_10_update', kwargs={'pk': self.object.pk}))

        return super().get(request, *args, **kwargs)


class TaskType_1_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/task_type_1.html'


class TaskType_2_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/task_type_2.html'


class TaskType_3_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/task_type_3.html'


class TaskType_4_UpdateView(UpdateView):
    pass


class TaskType_5_UpdateView(UpdateView):
    pass


class TaskType_6_UpdateView(UpdateView):
    pass


class TaskType_7_UpdateView(UpdateView):
    pass


class TaskType_8_UpdateView(UpdateView):
    pass


class TaskType_9_UpdateView(UpdateView):
    pass


class TaskType_10_UpdateView(UpdateView):
    pass