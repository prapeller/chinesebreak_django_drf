from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import BaseDeleteView

from adminpanel.forms import WordForm, GrammarForm, TopicForm, LessonForm, SelectTaskTypeForm, CourseForm, LangForm
from structure.models import Lang, Course, Topic, Lesson, Task
from elements.models import Word, Grammar, Character
import requests


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
    form_class = LangForm
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


def redirect_to_task_type(task_type, task_pk):
    return HttpResponseRedirect(reverse_lazy(f'adminpanel:task_type_{task_type}_update', kwargs={'pk': task_pk}))


class LessonUpdateView(UpdateView):
    extra_context = {'title': 'Lesson update',
                     'select_task_type_form': SelectTaskTypeForm,
                     'words_task_type_list': ['1', '2', '3', '4', '5'],
                     'sent_task_type_list': ['6', '7', '8', '9', '10', '11', '12', '13', '14'],
                     'dialog_task_type_list': ['15', '16', '17', '18'],
                     'puzzle_task_type_list': ['19', '20', '21'],
                     }
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
            return redirect_to_task_type(task_type, new_task.pk)


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
        return redirect_to_task_type(task_type, self.object.pk)


class TaskType_1_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/1_word_image.html'
    extra_context = {
        'title': '1_word_image',
    }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_words = Word.objects.filter(id__in=self.object.words)
        self.extra_context.update(task_words = task_words) if task_words else [],
        return super().get(request, *args, **kwargs)


class TaskType_2_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/2_word_char_from_lang.html'


class TaskType_3_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/3_word_lang_from_char.html'


class TaskType_4_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/4_word_char_from_video.html'


class TaskType_5_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/5_word_match.html'


class TaskType_6_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/6_sent_image.html'


class TaskType_7_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/7_sent_char_from_lang.html'


class TaskType_8_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/8_sent_lang_from_char.html'


class TaskType_9_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/9_sent_lang_from_video.html'


class TaskType_10_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/10_sent_say_from_char.html'


class TaskType_11_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/11_sent_say_from_video.html'


class TaskType_12_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/12_sent_paste_from_char.html'


class TaskType_13_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/13_sent_choose_from_char.html'


class TaskType_14_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/14_sent_delete_from_char.html'


class TaskType_15_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/15_dialog_A_char_from_char.html'


class TaskType_16_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/16_dialog_B_char_from_video.html'


class TaskType_17_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/17_dialog_A_puzzle_char_from_char.html'


class TaskType_18_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/18_dialog_B_puzzle_char_from_char.html'


class TaskType_19_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/19_puzzle_char_from_lang.html'


class TaskType_20_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/20_puzzle_lang_from_char.html'


class TaskType_21_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/21_puzzle_char_from_video.html'


class TaskType_22_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/22_word_write_from_video.html'


class TaskType_23_UpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'structure/tasks/23_grammar_choose_from_video.html'








class WordListView(ListView):
    model = Word
    extra_context = {'title': 'Word list'}
    ordering = ['id']


class WordCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        self.object = Word.objects.create(
            char='新的',
            pinyin='xīn de',
            lang='translation',
            lit='literal translation',
        )
        return HttpResponseRedirect(reverse_lazy('adminpanel:word_update', kwargs={'pk': self.object.pk}))


class WordUpdateView(UpdateView):
    model = Word
    form_class = WordForm
    extra_context = {'title': 'Word update'}

    def form_valid(self, form):
        self.object = form.save()
        if form.data.get('audio_url') and not form.data.get('audio'):
            self.object.save_audio_with_url(form.data.get('audio_url'))
        if self.request.POST.get('image_url') and not self.request.POST.get('image'):
            self.object.save_image_with_url(form.data.get('image_url'))
        self.success_url = reverse_lazy('adminpanel:word_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        task_type = request.POST.get('task_type')
        if task_type:
            new_task = Task.objects.create(
                task_type=task_type,
                creator=request.user,
                word=self.object,
            )
            return redirect_to_task_type(task_type, new_task.pk)
        return super().post(request, *args, **kwargs)


class WordDeleteView(BaseDeleteView):
    model = Word
    success_url = reverse_lazy('adminpanel:word_list')


class GrammarListView(ListView):
    model = Grammar
    extra_context = {'title': 'Grammar list'}


class GrammarCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        self.object = Grammar.objects.create(
            name='name',
            explanation = 'explanation',
            char = 'char',
            pinyin = 'pinyin',
            lang = 'lang',
            lit = 'lit',
            structure = 'structure',
        )
        return HttpResponseRedirect(reverse_lazy('adminpanel:grammar_update', kwargs={'pk': self.object.pk}))


class GrammarUpdateView(UpdateView):
    model = Grammar
    form_class = GrammarForm
    extra_context = {'title': 'Grammar update'}

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse_lazy('adminpanel:grammar_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        task_type = request.POST.get('task_type')
        if task_type:
            new_task = Task.objects.create(
                task_type=task_type,
                creator=request.user,
                grammar=self.object,
            )
            return redirect_to_task_type(task_type, new_task.pk)
        return super().post(request, *args, **kwargs)


class GrammarDeleteView(BaseDeleteView):
    model = Grammar
    success_url = reverse_lazy('adminpanel:grammar_list')


