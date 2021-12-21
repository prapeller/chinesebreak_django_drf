from django.urls import path
from .views import LangListView

app_name = 'lang'

urlpatterns = [
    path('lang-list/', LangListView.as_view(), name='lang_list'),
]