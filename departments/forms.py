from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        } 