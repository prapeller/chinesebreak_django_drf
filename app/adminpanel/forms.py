from django import forms

from structure.models import Lang, Course, Topic, Lesson, Task


class LangForm(forms.ModelForm):
    class Meta:
        model = Lang
        fields = '__all__'


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name',)

    def save(self, commit=True):
        return super().save()


class TopicForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Topic
        fields = ('name', 'image')


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('topic',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task_type',)
