from django import forms

from structure.models import Lang, Course, Topic, Lesson, Task


class LangForm(forms.ModelForm):
    name = forms.CharField(label='name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Lang
        fields = ('name',)


class CourseForm(forms.ModelForm):
    name = forms.CharField(label='name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Course
        fields = ('name',)

    def save(self, commit=True):
        return super().save()


class TopicForm(forms.ModelForm):
    name = forms.CharField(label='name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.FileField(label='image', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Topic
        fields = ('image', 'name')


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('topic',)


class TaskTypeForm(forms.ModelForm):
    task_type = forms.ChoiceField(choices=Task.TASK_TYPES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Task
        fields = ('task_type',)
