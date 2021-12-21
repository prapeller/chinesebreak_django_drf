class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'