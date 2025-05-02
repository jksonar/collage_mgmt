from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'established_date', 
                 'head_of_department', 'contact_email', 'contact_phone']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'established_date': forms.DateInput(attrs={'type': 'date'}),
        } 