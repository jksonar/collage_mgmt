from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'department', 'credits', 'description', 'duration', 'prerequisites']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'prerequisites': forms.SelectMultiple(attrs={'class': 'form-select'}),
        } 