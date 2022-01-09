from django import forms

from structure.models import Lang, Course, Topic, Lesson


class LangForm(forms.ModelForm):
    class Meta:
        model = Lang
        fields = '__all__'


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
