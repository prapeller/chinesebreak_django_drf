from http import cookies

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from app.mixin import TitleContextMixin, IsStuffDispatchMixin, IsSuperuserDispatchMixin
from django.urls import reverse_lazy

from core.models import Lang, LangForm, Course, CourseForm, Topic, TopicForm, Lesson


def lang_list_view(request):
    lang_list = Lang.objects.all().order_by('pk')
    context = {
        'title': 'admin panel',
        'lang_list': lang_list,
    }
    return render(request, 'admin_panel/index.html', context)


def lang_form_view(request, pk=None):
    lang = Lang.objects.filter(pk=pk).first() if pk else Lang(creator=request.user)
    courses = Course.objects.filter(lang_id=lang.pk)
    form = LangForm(instance=lang)
    if request.method == 'POST':
        form = LangForm(data=request.POST, instance=lang)
        if form.is_valid():
            form.save()

    request.session['lang_id'] = lang.pk
    context = {
        'form': form,
        'lang': lang,
        'courses': courses,
    }

    return render(request, 'admin_panel/lang.html', context)


def lang_delete_view(request, pk):
    lang = Lang.objects.get(pk=pk)
    lang.delete()
    return redirect('admin_panel:lang_list')


def course_form_view(request, pk=None):
    lang_id = request.session.get('lang_id')
    course = Course.objects.filter(pk=pk).first() if pk else Course(creator=request.user, lang_id=lang_id)
    topics = Topic.objects.filter(course_id=course.pk)
    form = CourseForm(instance=course)
    if request.method == 'POST':
        form = CourseForm(data=request.POST, instance=course)
        if form.is_valid():
            form.save()

    request.session['course_id'] = course.pk
    context = {
        'form': form,
        'course': course,
        'topics': topics,
    }

    return render(request, 'admin_panel/course.html', context)


def course_delete_view(request, pk):
    course = Course.objects.get(pk=pk)
    lang_id = course.lang_id
    return redirect('admin_panel:lang_update', pk=lang_id)


def topic_form_view(request, pk=None):
    topic = Topic.objects.filter(pk=pk).first() if pk else Topic(creator=request.user)
    lessons = Lesson.objects.filter(topic_id=topic.pk)
    form = TopicForm(instance=topic)
    if request.method == 'POST':
        form = CourseForm(data=request.POST, instance=topic)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
        'topic': topic,
        'lessons': lessons,
    }

    return render(request, 'admin_panel/course.html', context)


def topic_delete_view(request, pk):
    topic = Topic.objects.get(pk=pk)
    course_id = topic.course_id
    topic.delete()
    return redirect('admin_panel:course_update', pk=course_id)


def lesson_form_view(request):
    return None


def lesson_delete_view(request):
    return None