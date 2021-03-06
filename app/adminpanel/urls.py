from django.urls import path

from adminpanel.views import (index,
                              WordCreateView, WordListView, WordUpdateView, WordDeleteView,
                              GrammarCreateView, GrammarListView, GrammarUpdateView, GrammarDeleteView,

                              LangCreateView, LangListView, LangUpdateView, LangDeleteView,
                              CourseCreateView, CourseUpdateView, CourseDeleteView,
                              TopicCreateView, TopicUpdateView, TopicDeleteView,
                              LessonCreateView, LessonUpdateView, LessonDeleteView,

                              TaskUpdateView,
                              task_update_with_ajax,
                              TaskType_1_UpdateView,
                              TaskType_2_UpdateView,
                              TaskType_3_UpdateView,
                              TaskType_4_UpdateView,
                              TaskType_5_UpdateView,
                              TaskType_6_UpdateView,
                              TaskType_7_UpdateView,
                              TaskType_8_UpdateView,
                              TaskType_9_UpdateView,
                              TaskType_10_UpdateView,
                              TaskType_11_UpdateView,
                              TaskType_12_UpdateView,
                              TaskType_13_UpdateView,
                              TaskType_14_UpdateView,
                              TaskType_15_UpdateView,
                              TaskType_16_UpdateView,
                              TaskType_17_UpdateView,
                              TaskType_18_UpdateView,
                              TaskType_19_UpdateView,
                              TaskType_20_UpdateView,
                              TaskType_21_UpdateView,
                              TaskType_22_UpdateView,
                              TaskType_23_UpdateView,
                              TaskDeleteView)

app_name = 'adminpanel'

urlpatterns = [
    path('', index, name='index'),

    path('elements/words/', WordListView.as_view(), name='word_list'),
    path('elements/words/create', WordCreateView.as_view(), name='word_create'),
    path('elements/words/update/<int:pk>/', WordUpdateView.as_view(), name='word_update'),
    path('elements/words/delete/<int:pk>/', WordDeleteView.as_view(), name='word_delete'),

    path('elements/grammars/', GrammarListView.as_view(), name='grammar_list'),
    path('elements/grammars/create', GrammarCreateView.as_view(), name='grammar_create'),
    path('elements/grammars/update/<int:pk>/', GrammarUpdateView.as_view(), name='grammar_update'),
    path('elements/grammars/delete/<int:pk>/', GrammarDeleteView.as_view(), name='grammar_delete'),

    path('structure/langs/', LangListView.as_view(), name='lang_list'),

    path('structure/langs/create/', LangCreateView.as_view(), name='lang_create'),
    path('structure/langs/update/<int:pk>/', LangUpdateView.as_view(), name='lang_update'),
    path('structure/langs/delete/<int:pk>/', LangDeleteView.as_view(), name='lang_delete'),

    path('structure/courses/create/', CourseCreateView.as_view(), name='course_create'),
    path('structure/courses/update/<int:pk>/', CourseUpdateView.as_view(), name='course_update'),
    path('structure/courses/delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),

    path('structure/topics/create/', TopicCreateView.as_view(), name='topic_create'),
    path('structure/topics/update/<int:pk>/', TopicUpdateView.as_view(), name='topic_update'),
    path('structure/topics/delete/<int:pk>/', TopicDeleteView.as_view(), name='topic_delete'),

    path('structure/lessons/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('structure/lessons/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('structure/lessons/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson_delete'),

    path('structure/tasks/update/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('structure/tasks/update_with_ajax/<int:pk>/', task_update_with_ajax, name='task_update_with_ajax'),

    path('structure/tasks/type_1/update/<int:pk>/', TaskType_1_UpdateView.as_view(), name='task_type_1_update'),
    path('structure/tasks/type_2/update/<int:pk>/', TaskType_2_UpdateView.as_view(), name='task_type_2_update'),
    path('structure/tasks/type_3/update/<int:pk>/', TaskType_3_UpdateView.as_view(), name='task_type_3_update'),
    path('structure/tasks/type_4/update/<int:pk>/', TaskType_4_UpdateView.as_view(), name='task_type_4_update'),
    path('structure/tasks/type_5/update/<int:pk>/', TaskType_5_UpdateView.as_view(), name='task_type_5_update'),
    path('structure/tasks/type_6/update/<int:pk>/', TaskType_6_UpdateView.as_view(), name='task_type_6_update'),
    path('structure/tasks/type_7/update/<int:pk>/', TaskType_7_UpdateView.as_view(), name='task_type_7_update'),
    path('structure/tasks/type_8/update/<int:pk>/', TaskType_8_UpdateView.as_view(), name='task_type_8_update'),
    path('structure/tasks/type_9/update/<int:pk>/', TaskType_9_UpdateView.as_view(), name='task_type_9_update'),
    path('structure/tasks/type_10/update/<int:pk>/', TaskType_10_UpdateView.as_view(), name='task_type_10_update'),
    path('structure/tasks/type_11/update/<int:pk>/', TaskType_11_UpdateView.as_view(), name='task_type_11_update'),
    path('structure/tasks/type_12/update/<int:pk>/', TaskType_12_UpdateView.as_view(), name='task_type_12_update'),
    path('structure/tasks/type_13/update/<int:pk>/', TaskType_13_UpdateView.as_view(), name='task_type_13_update'),
    path('structure/tasks/type_14/update/<int:pk>/', TaskType_14_UpdateView.as_view(), name='task_type_14_update'),
    path('structure/tasks/type_15/update/<int:pk>/', TaskType_15_UpdateView.as_view(), name='task_type_15_update'),
    path('structure/tasks/type_16/update/<int:pk>/', TaskType_16_UpdateView.as_view(), name='task_type_16_update'),
    path('structure/tasks/type_17/update/<int:pk>/', TaskType_17_UpdateView.as_view(), name='task_type_17_update'),
    path('structure/tasks/type_18/update/<int:pk>/', TaskType_18_UpdateView.as_view(), name='task_type_18_update'),
    path('structure/tasks/type_19/update/<int:pk>/', TaskType_19_UpdateView.as_view(), name='task_type_19_update'),
    path('structure/tasks/type_20/update/<int:pk>/', TaskType_20_UpdateView.as_view(), name='task_type_20_update'),
    path('structure/tasks/type_21/update/<int:pk>/', TaskType_21_UpdateView.as_view(), name='task_type_21_update'),
    path('structure/tasks/type_22/update/<int:pk>/', TaskType_22_UpdateView.as_view(), name='task_type_22_update'),
    path('structure/tasks/type_23/update/<int:pk>/', TaskType_23_UpdateView.as_view(), name='task_type_23_update'),
    path('structure/tasks/delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
]
