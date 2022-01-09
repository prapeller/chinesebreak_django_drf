from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin
from django.shortcuts import render
from django.contrib.auth import get_user_model

from structure.models import Lang


def index(request):
    context = {'title': 'Main'}
    return render(request, 'index.html', context)


class LangListView(ListView):
    model = Lang
    extra_context = {'title': 'Lang list'}


class LangCreateView(CreateView):
    model = Lang
    extra_context = {'title': 'Lang create'}


class LangUpdateView(UpdateView):
    model = Lang
    extra_context = {'title': 'Lang update'}


class LangDeleteView(DeleteView):
    model = Lang
    extra_context = {'title': 'Lang delete'}
