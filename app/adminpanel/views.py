from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import BaseDeleteView

from adminpanel.forms import WordForm, GrammarForm, TopicForm, SelectTaskTypeForm, CourseForm, LangForm, TaskForm
from elements.models import Word, Grammar
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
        self.extra_context.update({'sub_object_list': Task.objects.filter(lesson=self.object).order_by('id')})
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
    model = Task
    fields = ()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_type = self.object.task_type
        return redirect_to_task_type(task_type, self.object.pk)


def task_update_with_ajax(request, pk):
    task = Task.objects.get(pk=pk)

    act_deact_word_idx = request.GET.get('act_deact_word_idx')
    act_deact_grammar_for_word_idx = request.GET.get('act_deact_grammar_for_word_idx')
    remove_word_idx = request.GET.get('remove_word_idx')
    add_word_id = request.GET.get('add_word_id')
    add_grammar_id = request.GET.get('add_grammar_id')
    remove_sent_image_idx = request.GET.get('remove_sent_image_idx')

    if act_deact_word_idx:
        idx = int(act_deact_word_idx)
        word = task.words[idx]
        word[1] = 0 if word[1] == 1 else 1
        task.save()

    if act_deact_grammar_for_word_idx:
        idx = int(act_deact_grammar_for_word_idx)
        word = task.words[idx]
        word[2] = 0 if word[2] == 1 else 1
        word_task_grammars = [word[2] for word in task.words]
        if not 1 in word_task_grammars:
            task.grammar = None
        task.save()

    if remove_word_idx:
        idx = int(remove_word_idx)
        task.words.pop(idx)
        task.save()

    if add_word_id:
        word_id = int(add_word_id)
        task.words.append([word_id, 0, 0])
        task.save()

    if add_grammar_id:
        id = int(add_grammar_id)
        task.grammar = Grammar.objects.get(id=id)
        task.save()

    if remove_sent_image_idx:
        idx = int(remove_sent_image_idx)
        task.sent_images.pop(idx)
        task.save()

    context = {'object': Task.objects.get(pk=pk),
               'task_words': [(idx, Word.objects.get(id=word[0]), word[1], word[2]) for idx, word in enumerate(task.words)],
               'task_grammar': task.grammar,
               'sent_images': task.sent_images,
               }
    task_words_html = render_to_string(f'structure/tasks/includes/task_words.html', context, request)
    active_elements_html = render_to_string(f'structure/tasks/includes/active_elements.html', context, request)
    sent_images_html = render_to_string(f'structure/tasks/includes/sent_images.html', context, request)
    return JsonResponse({
        'active_elements_html': active_elements_html,
        'task_words_html': task_words_html,
        'sent_images_html': sent_images_html,
    })


class TaskType_1_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.task_type}_{self.object.get_task_type_display()}.html'
        self.extra_context.update({
            'title': f'{self.object.task_type}_{self.object.get_task_type_display}',
            'task_words': [(idx, Word.objects.get(id=word[0]), word[1], word[2]) for idx, word in enumerate(self.object.words)],
            'words': Word.objects.all(),
        })
        return super().get(request, *args, **kwargs)


class TaskType_2_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.task_type}_{self.object.get_task_type_display()}.html'
        self.extra_context.update({
            'title': f'{self.object.task_type}_{self.object.get_task_type_display}',
            'task_words': [(idx, Word.objects.get(id=word[0]), word[1], word[2]) for idx, word in enumerate(self.object.words)],
            'words': Word.objects.all(),
        })
        return super().get(request, *args, **kwargs)


class TaskType_3_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.task_type}_{self.object.get_task_type_display()}.html'
        self.extra_context.update({
            'title': f'{self.object.task_type}_{self.object.get_task_type_display}',
            'task_words': [(idx, Word.objects.get(id=word[0]), word[1], word[2]) for idx, word in enumerate(self.object.words)],
            'words': Word.objects.all(),
        })
        return super().get(request, *args, **kwargs)


class TaskType_4_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.task_type}_{self.object.get_task_type_display()}.html'
        self.success_url = reverse_lazy('adminpanel:task_type_4_update', kwargs={'pk': self.object.pk})
        self.extra_context.update({
            'video_form': TaskForm(instance=self.object),
            'title': f'{self.object.task_type}_{self.object.get_task_type_display}',
            'task_words': [(idx, Word.objects.get(id=word[0]), word[1], word[2]) for idx, word in enumerate(self.object.words)],
            'words': Word.objects.all(),
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        file = form.files.get('video')
        url = form.data.get('video_url')
        if file:
            self.object.save_video_with_file(file)
        if url and not file:
            self.object.save_video_with_url(url)
        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_5_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.task_type}_{self.object.get_task_type_display()}.html'
        self.extra_context.update({
            'title': f'{self.object.task_type}_{self.object.get_task_type_display}',
            'task_words': [(idx, Word.objects.get(id=word[0]), word[1], word[2]) for idx, word in enumerate(self.object.words)],
            'words': Word.objects.all(),
        })
        return super().get(request, *args, **kwargs)


class TaskType_6_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.task_type}_{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.task_type}_{self.object.get_task_type_display}',
            'form': TaskForm(instance=self.object),
            'sent_images': self.object.sent_images,
            'task_words': [(idx, Word.objects.get(id=word[0]), word[1], word[2]) for idx, word in enumerate(self.object.words)],
            'task_grammar': self.object.grammar,
            'words': Word.objects.all(),
            'grammars': Grammar.objects.all(),
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_image(
            image_file=form.files.get('image'),
            image_url=form.data.get('image_url')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


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
        if form.data.get('audio_url') and not form.files.get('audio'):
            self.object.save_audio_with_url(form.data.get('audio_url'))
        if form.data.get('image_url') and not form.files.get('image'):
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
            explanation='explanation',
            char='char',
            pinyin='pinyin',
            lang='lang',
            lit='lit',
            structure='structure',
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
