from django.urls import path

from adminpanel.views import (index, LangCreateView, LangListView, LangUpdateView, LangDeleteView,
                              CourseCreateView, CourseUpdateView, CourseDeleteView,
                              TopicCreateView, TopicUpdateView, TopicDeleteView,
                              LessonCreateView, LessonUpdateView, LessonDeleteView,

                              TaskUpdateView,
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
                              TaskDeleteView)

app_name = 'adminpanel'

urlpatterns = [
    path('', index, name='index'),

    path('structure/langs/', LangListView.as_view(), name='lang_list'),

    path('structure/langs/create', LangCreateView.as_view(), name='lang_create'),
    path('structure/langs/update/<int:pk>/', LangUpdateView.as_view(), name='lang_update'),
    path('structure/langs/delete/<int:pk>/', LangDeleteView.as_view(), name='lang_delete'),

    path('structure/courses/create', CourseCreateView.as_view(), name='course_create'),
    path('structure/courses/update/<int:pk>/', CourseUpdateView.as_view(), name='course_update'),
    path('structure/courses/delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),

    path('structure/topics/create', TopicCreateView.as_view(), name='topic_create'),
    path('structure/topics/update/<int:pk>/', TopicUpdateView.as_view(), name='topic_update'),
    path('structure/topics/delete/<int:pk>/', TopicDeleteView.as_view(), name='topic_delete'),

    path('structure/lessons/create', LessonCreateView.as_view(), name='lesson_create'),
    path('structure/lessons/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('structure/lessons/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson_delete'),

    path('structure/tasks/update/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
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
    path('structure/tasks/delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
]
