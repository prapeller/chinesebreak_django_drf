from django.contrib import admin
from django.urls import path, include
from .views import \
    lang_list_view, lang_form_view, lang_delete_view, \
    course_form_view, course_delete_view, \
    topic_form_view, topic_delete_view, \
    lesson_form_view, lesson_delete_view

app_name = 'admin_panel'

urlpatterns = [
    path('', lang_list_view, name='lang_list'),
    path('langs/', lang_list_view, name='lang_list'),
    path('langs/form/', lang_form_view, name='lang_create'),
    path('langs/form/<int:pk>', lang_form_view, name='lang_update'),
    path('langs/delete/<int:pk>/', lang_delete_view, name='lang_delete'),

    path('courses/form/', course_form_view, name='course_create'),
    path('courses/form/<int:pk>/', course_form_view, name='course_update'),
    path('courses/delete/<int:pk>/', course_delete_view, name='course_delete'),

    path('topics/form/', topic_form_view, name='topic_create'),
    path('topics/form/<int:pk>/', topic_form_view, name='topic_update'),
    path('topics/delete/<int:pk>/', topic_delete_view, name='topic_delete'),

    path('lessons/form/', lesson_form_view, name='lesson_create'),
    path('lessons/form/<int:pk>/', lesson_form_view, name='lesson_update'),
    path('topics/delete/<int:pk>/', lesson_delete_view, name='topic_delete'),
]
