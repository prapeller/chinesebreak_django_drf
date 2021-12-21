from django.shortcuts import render
from django.views.generic import ListView

from structure.lang.models import Lang


class LangListView(ListView):
    model = Lang
    # context_object_name = 'langs'
    # template_name = 'lang/lang_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Languages'
        return context