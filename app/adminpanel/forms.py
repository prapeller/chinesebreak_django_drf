from django import forms

from structure.models import Lang, Course, Topic, Lesson, Task
from elements.models import Word, Grammar, Character


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


class SelectTaskTypeForm(forms.Form):
    task_type = forms.CharField(widget=forms.Select(choices=Task.TASK_TYPES, attrs={'class': 'form-select'}))


class WordForm(forms.ModelForm):
    pinyin = forms.CharField(label='pinyin', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    char = forms.CharField(label='char', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    lang = forms.CharField(label='lang', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    lit = forms.CharField(label='lit', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    image = forms.FileField(label='image', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image_url = forms.URLField(label='image_url', widget=forms.URLInput(attrs={'class': 'form-control'}),
                               required=False)

    audio = forms.FileField(label='audio', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    audio_url = forms.URLField(label='audio_url', widget=forms.URLInput(attrs={'class': 'form-control'}),
                               required=False)

    video = forms.FileField(label='video', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    video_url = forms.URLField(label='video_url', widget=forms.URLInput(attrs={'class': 'form-control'}),
                               required=False)

    class Meta:
        model = Word
        fields = '__all__'


class GrammarForm(forms.ModelForm):
    name = forms.CharField(label='name', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    explanation = forms.CharField(label='explanation', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=False)
    char = forms.CharField(label='char', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    pinyin = forms.CharField(label='pinyin', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    lang = forms.CharField(label='lang', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    lit = forms.CharField(label='lit', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    structure = forms.CharField(label='structure', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                required=False)

    class Meta:
        model = Grammar
        fields = '__all__'
