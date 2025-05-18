from django import forms
from .models import Attendance
from students.models import Student
from courses.models import Course
from django.utils import timezone

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter remarks if any'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()
        self.fields['student'].queryset = Student.objects.filter(is_active=True)
        self.fields['course'].queryset = Course.objects.filter(is_active=True)

class AttendanceFilterForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        required=False,
        empty_label='All Courses'
    )
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(Attendance.STATUS_CHOICES),
        required=False
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    department = forms.ModelChoiceField(
        queryset=Course.objects.values_list('department', flat=True).distinct(),
        required=False,
        empty_label='All Departments'
    ) 