from django.urls import path

from adminpanel.views import index, LangCreateView, LangListView, LangUpdateView, LangDeleteView


app_name = 'adminpanel'

urlpatterns = [
    path('', index),
    path('structure/langs/', LangListView.as_view(), name='lang_list'),
    path('structure/langs-create/', LangCreateView.as_view(), name='lang_create'),
    path('structure/langs-update/<int:pk>/', LangUpdateView.as_view(), name='lang_update'),
    path('structure/langs-delete/<int:pk>/', LangDeleteView.as_view(), name='lang_delete'),
]
