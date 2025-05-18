from django import forms
from .models import Faculty
from departments.models import Department

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['user', 'department', 'employee_id', 'designation', 'specialization', 
                 'joining_date', 'qualification', 'experience', 'contact_number', 'address']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter address'}),
            'specialization': forms.TextInput(attrs={'placeholder': 'Enter specialization area'}),
            'qualification': forms.TextInput(attrs={'placeholder': 'Enter qualification'}),
            'employee_id': forms.TextInput(attrs={'placeholder': 'Enter employee ID'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()
        self.fields['user'].queryset = self.fields['user'].queryset.filter(groups__name='Faculty') 