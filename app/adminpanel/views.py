from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
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
    if act_deact_word_idx:
        idx = int(act_deact_word_idx)
        word = task.words[idx]
        word[1] = 0 if word[1] == 1 else 1
        task.save()

    act_deact_grammar_for_word_idx = request.GET.get('act_deact_grammar_for_word_idx')
    if act_deact_grammar_for_word_idx:
        idx = int(act_deact_grammar_for_word_idx)
        word = task.words[idx]
        word[2] = 0 if word[2] == 1 else 1
        word_task_grammars = [word[2] for word in task.words]
        if not 1 in word_task_grammars:
            task.grammar = None
        task.save()

    act_deact_to_display_word_idx = request.GET.get('act_deact_to_display_word_idx')
    if act_deact_to_display_word_idx:
        idx = int(act_deact_to_display_word_idx)
        word = task.words[idx]
        word[3] = 0 if word[3] == 1 else 1
        task.save()

    act_deact_to_delete_word_idx = request.GET.get('act_deact_to_delete_word_idx')
    if act_deact_to_delete_word_idx:
        idx = int(act_deact_to_delete_word_idx)
        word = task.words[idx]
        word[4] = 0 if word[4] == 1 else 1
        task.save()

    remove_word_idx = request.GET.get('remove_word_idx')
    if remove_word_idx:
        idx = int(remove_word_idx)
        task.words.pop(idx)
        task.save()

    add_word_id = request.GET.get('add_word_id')
    if add_word_id:
        word_id = int(add_word_id)
        task.words.append([word_id, 0, 0, 0, 0])
        task.save()

    add_grammar_id = request.GET.get('add_grammar_id')
    if add_grammar_id:
        id = int(add_grammar_id)
        task.grammar = Grammar.objects.get(id=id)
        task.save()

    remove_sent_image_idx = request.GET.get('remove_sent_image_idx')
    if remove_sent_image_idx:
        idx = int(remove_sent_image_idx)
        task.sent_images.pop(idx)
        task.save()

    remove_sent_wrong_idx = request.GET.get('remove_sent_wrong_idx')
    if remove_sent_wrong_idx:
        idx = int(remove_sent_wrong_idx)
        task.sent_wrong.pop(idx)
        task.save()

    search_wrong_words = request.GET.get('search_wrong_words')
    search_wrong_words_list = []
    if search_wrong_words:
        search_wrong_words_list = Word.objects.filter(
            Q(pinyin__icontains=search_wrong_words) | Q(char__icontains=search_wrong_words) | Q(lang__icontains=search_wrong_words)
        )

    search_words = request.GET.get('search_words')
    search_words_list = []
    if search_words:
        search_words_list = Word.objects.filter(
            Q(pinyin__icontains=search_words) | Q(char__icontains=search_words) | Q(lang__icontains=search_words)
        )

    search_grammars = request.GET.get('search_grammars')
    search_grammars_list = []
    if search_grammars:
        search_grammars_list = Grammar.objects.filter(
            Q(name__icontains=search_grammars) | Q(pinyin__icontains=search_grammars) | Q(char__icontains=search_grammars) | Q(
                lang__icontains=search_grammars)
        )

    remove_wrong_word = request.GET.get('remove_wrong_word')
    if remove_wrong_word:
        word_pk = int(remove_wrong_word)
        task.words_wrong.remove(word_pk)
        task.save()

    add_wrong_word_word_id = request.GET.get('add_wrong_word_word_id')
    if add_wrong_word_word_id:
        task.words_wrong.append(int(add_wrong_word_word_id))
        task.save()

    remove_lang_puzzle_word_right = request.GET.get('remove_lang_puzzle_word_right')
    if remove_lang_puzzle_word_right:
        idx = int(remove_lang_puzzle_word_right)
        task.lang_puzzle_words_right.pop(idx)
        task.save()

    remove_lang_puzzle_word_wrong = request.GET.get('remove_lang_puzzle_word_wrong')
    if remove_lang_puzzle_word_wrong:
        idx = int(remove_lang_puzzle_word_wrong)
        task.lang_puzzle_words_wrong.pop(idx)
        task.save()

    context = {'object': Task.objects.get(pk=pk),
               'task_words': task.get_task_words(),
               'task_grammar': task.grammar,
               'sent_images': task.sent_images,
               'sent_right': task.get_right_sent_from_task_words(),
               'sent_wrong_list': task.sent_wrong,
               'active_words': [word[1] for word in task.get_task_words() if word[2] == 1],
               'wrong_words': [Word.objects.get(id=word_id) for word_id in task.words_wrong],
               'search_wrong_words_list': search_wrong_words_list,
               'search_words_list': search_words_list,
               'search_grammars_list': search_grammars_list,
               'lang_puzzle_words_right': task.lang_puzzle_words_right,
               'lang_puzzle_words_wrong': task.lang_puzzle_words_wrong,
               }

    task_words_html = ''
    if task.task_type in ('1', '2', '3', '4', '5'):
        task_words_html = render_to_string(f'structure/tasks/includes/task_words_active_words.html', context, request)
    if task.task_type in ('6', '7', '8', '9', '13', '15', '16', '20'):
        task_words_html = render_to_string(f'structure/tasks/includes/task_words_active_words_grammared_words.html', context, request)
    if task.task_type in ('10', '11', '12', '17', '18', '19', '21'):
        task_words_html = render_to_string(f'structure/tasks/includes/task_words_active_words_grammared_words_to_display_words.html',
                                           context, request)
    if task.task_type in ('14',):
        task_words_html = render_to_string(
            f'structure/tasks/includes/task_words_active_words_grammared_words_to_display_words_to_delete_words.html', context, request)
    if task.task_type in ('22',):
        task_words_html = render_to_string(f'structure/tasks/includes/task_words_to_display_words.html', context, request)

    search_wrong_words_list_html = render_to_string(f'structure/tasks/includes/search_wrong_words_list.html', context, request)
    wrong_words_html = render_to_string(f'structure/tasks/includes/wrong_words.html', context, request)
    search_words_list_html = render_to_string(f'structure/tasks/includes/search_words_list.html', context, request)
    search_grammars_list_html = render_to_string(f'structure/tasks/includes/search_grammars_list.html', context, request)
    active_elements_html = render_to_string(f'structure/tasks/includes/active_elements.html', context, request)
    sent_images_html = render_to_string(f'structure/tasks/includes/sent_images.html', context, request)

    task_sents_html = ''
    if any([x in task.get_task_type_display() for x in ['dialog_A']]):
        task_sents_html = render_to_string(f'structure/tasks/includes/task_sents_dialog_from_lang.html', context, request)
    if any([x in task.get_task_type_display() for x in ['dialog_B']]):
        task_sents_html = render_to_string(f'structure/tasks/includes/task_sents_dialog_from_video.html', context, request)
    if any([x in task.get_task_type_display() for x in ['from_lang']]):
        task_sents_html = render_to_string(f'structure/tasks/includes/task_sents_from_lang.html', context, request)
    if any([x in task.get_task_type_display() for x in ['from_char', 'from_video']]):
        task_sents_html = render_to_string(f'structure/tasks/includes/task_sents_from_char.html', context, request)

    lang_puzzle_words_right_html = render_to_string(f'structure/tasks/includes/lang_puzzle_words_right.html', context, request)
    lang_puzzle_words_wrong_html = render_to_string(f'structure/tasks/includes/lang_puzzle_words_wrong.html', context, request)

    return JsonResponse({
        'active_elements_html': active_elements_html,
        'task_words_html': task_words_html,
        'sent_images_html': sent_images_html,
        'task_sents_html': task_sents_html,
        'wrong_words_html': wrong_words_html,
        'search_wrong_words_list_html': search_wrong_words_list_html,
        'search_words_list_html': search_words_list_html,
        'search_grammars_list_html': search_grammars_list_html,
        'lang_puzzle_words_right_html': lang_puzzle_words_right_html,
        'lang_puzzle_words_wrong_html': lang_puzzle_words_wrong_html,
    })


class TaskType_1_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'
        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'task_words': self.object.get_task_words(),
        })
        return super().get(request, *args, **kwargs)


class TaskType_2_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'
        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'task_words': self.object.get_task_words(),
        })
        return super().get(request, *args, **kwargs)


class TaskType_3_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'
        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'task_words': self.object.get_task_words(),
        })
        return super().get(request, *args, **kwargs)


class TaskType_4_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'
        self.success_url = reverse_lazy('adminpanel:task_type_4_update', kwargs={'pk': self.object.pk})
        self.extra_context.update({
            'form': TaskForm(instance=self.object),
            'title': f'{self.object.get_task_type_display()}',
            'task_words': self.object.get_task_words(),
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_video(
            video_file=form.files.get('video'),
            video_url=form.data.get('video_url')
        )
        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_5_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'
        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'task_words': self.object.get_task_words(),
        })
        return super().get(request, *args, **kwargs)


class TaskType_6_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'sent_images': self.object.sent_images,
            'task_words': self.object.get_task_words(),
            'task_grammar': self.object.grammar,
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
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'task_words': self.object.get_task_words(),
            'task_grammar': self.object.grammar,
            'sent_right': self.object.get_right_sent_from_task_words(),
            'sent_wrong_list': self.object.sent_wrong,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.add_sent_wrong(
            sent_wrong_pinyin=form.data.get('sent_wrong_pinyin'),
            sent_wrong_char=form.data.get('sent_wrong_char')
        )

        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_8_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'task_words': self.object.get_task_words(),
            'task_grammar': self.object.grammar,
            'sent_right': self.object.sent_lang_A,
            'sent_wrong_list': self.object.sent_wrong,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.add_sent_wrong(
            sent_wrong_lang=form.data.get('sent_wrong_lang'),
        )

        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_9_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'task_words': self.object.get_task_words(),
            'task_grammar': self.object.grammar,
            'sent_right': self.object.sent_lang_A,
            'sent_wrong_list': self.object.sent_wrong,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_video(
            video_file=form.files.get('video'),
            video_url=form.data.get('video_url')
        )

        self.object.add_sent_wrong(
            sent_wrong_lang=form.data.get('sent_wrong_lang'),
        )

        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_10_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'task_words': self.object.get_task_words(),
            'task_grammar': self.object.grammar,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_11_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'task_words': self.object.get_task_words(),
            'task_grammar': self.object.grammar,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_video(
            video_file=form.files.get('video'),
            video_url=form.data.get('video_url')
        )

        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_12_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'task_words': self.object.get_task_words(),
            'task_grammar': self.object.grammar,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_13_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'
        task_words = self.object.get_task_words()

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'active_words': [word[1] for word in task_words if word[2] == 1],
            'wrong_words': [Word.objects.get(id=word_id) for word_id in self.object.words_wrong],
            'task_words': task_words,
            'task_grammar': self.object.grammar,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_14_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'
        task_words = self.object.get_task_words()

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'active_words': [word[1] for word in task_words if word[2] == 1],
            'task_words': task_words,
            'task_grammar': self.object.grammar,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_15_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'task_words': self.object.get_task_words(),
            'task_grammar': self.object.grammar,
            'sent_right': self.object.get_right_sent_from_task_words(),
            'sent_wrong_list': self.object.sent_wrong,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.add_sent_wrong(
            sent_wrong_pinyin=form.data.get('sent_wrong_pinyin'),
            sent_wrong_char=form.data.get('sent_wrong_char')
        )

        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A'),
            sent_char_B=form.data.get('sent_char_B'),
            sent_pinyin_B=form.data.get('sent_pinyin_B'),
            sent_lang_B=form.data.get('sent_lang_B'),
            sent_lit_B=form.data.get('sent_lit_B'),

        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url'),
            sent_audio_B_file=form.files.get('sent_audio_B_file'),
            sent_audio_B_url=form.data.get('sent_audio_B_url'),
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_16_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'task_words': self.object.get_task_words(),
            'task_grammar': self.object.grammar,
            'sent_right': self.object.get_right_sent_from_task_words(),
            'sent_wrong_list': self.object.sent_wrong,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_video(
            video_file=form.files.get('video'),
            video_url=form.data.get('video_url')
        )

        self.object.add_sent_wrong(
            sent_wrong_pinyin=form.data.get('sent_wrong_pinyin'),
            sent_wrong_char=form.data.get('sent_wrong_char')
        )

        self.object.save_task_sent(
            sent_char_A=form.data.get('sent_char_A'),
            sent_pinyin_A=form.data.get('sent_pinyin_A'),
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A'),

            sent_lang_B=form.data.get('sent_lang_B'),
            sent_lit_B=form.data.get('sent_lit_B'),
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url'),
            sent_audio_B_file=form.files.get('sent_audio_B_file'),
            sent_audio_B_url=form.data.get('sent_audio_B_url'),
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_17_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'task_words': self.object.get_task_words(),
            'task_grammar': self.object.grammar,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A'),
            sent_char_B=form.data.get('sent_char_B'),
            sent_pinyin_B=form.data.get('sent_pinyin_B'),
            sent_lang_B=form.data.get('sent_lang_B'),
            sent_lit_B=form.data.get('sent_lit_B'),
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url'),
            sent_audio_B_file=form.files.get('sent_audio_B'),
            sent_audio_B_url=form.data.get('sent_audio_B_url'),
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_18_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'task_words': self.object.get_task_words(),
            'task_grammar': self.object.grammar,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A'),
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url'),
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_19_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'
        task_words = self.object.get_task_words()

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'active_words': [word[1] for word in task_words if word[2] == 1],
            'wrong_words': [Word.objects.get(id=word_id) for word_id in self.object.words_wrong],
            'task_words': task_words,
            'task_grammar': self.object.grammar,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_20_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'
        task_words = self.object.get_task_words()

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'active_words': [word[1] for word in task_words if word[2] == 1],
            'lang_puzzle_words_right': [word for word in self.object.lang_puzzle_words_right],
            'lang_puzzle_words_wrong': [word for word in self.object.lang_puzzle_words_wrong],
            'task_words': task_words,
            'task_grammar': self.object.grammar,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.object.add_lang_puzzle_word(
            lang_puzzle_word_right=form.data.get('lang_puzzle_word_right'),
            lang_puzzle_word_wrong=form.data.get('lang_puzzle_word_wrong'),
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_21_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'
        task_words = self.object.get_task_words()

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'active_words': [word[1] for word in task_words if word[2] == 1],
            'wrong_words': [Word.objects.get(id=word_id) for word_id in self.object.words_wrong],
            'task_words': task_words,
            'task_grammar': self.object.grammar,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.object.save_task_video(
            video_file=form.files.get('video'),
            video_url=form.data.get('video_url')
        )

        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class TaskType_22_UpdateView(UpdateView):
    model = Task
    fields = ()
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.template_name = f'structure/tasks/{self.object.get_task_type_display()}.html'
        task_words = self.object.get_task_words()

        self.extra_context.update({
            'title': f'{self.object.get_task_type_display()}',
            'form': TaskForm(instance=self.object),
            'active_word': self.object.word,
            'task_words': task_words,
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.save_task_sent(
            sent_lang_A=form.data.get('sent_lang_A'),
            sent_lit_A=form.data.get('sent_lit_A')
        )

        self.object.save_task_audio(
            sent_audio_A_file=form.files.get('sent_audio_A'),
            sent_audio_A_url=form.data.get('sent_audio_A_url')
        )

        self.object.save_task_video(
            video_file=form.files.get('video'),
            video_url=form.data.get('video_url')
        )
        self.success_url = reverse_lazy(f'adminpanel:task_type_{self.object.task_type}_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


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
            task, is_created = Task.objects.get_or_create(
                task_type=task_type,
                creator=request.user,
                word=self.get_object(),
            )
            return redirect_to_task_type(task_type, task.pk)
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
