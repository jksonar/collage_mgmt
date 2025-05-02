from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, StudentEnrollment
from departments.models import Department, DepartmentProgram

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'roll_number', 'department', 'program', 'date_of_birth', 'gender',
            'blood_group', 'phone_number', 'emergency_contact', 'address',
            'nationality', 'religion', 'father_name', 'mother_name',
            'guardian_name', 'guardian_relation', 'guardian_phone',
            'guardian_address', 'previous_qualification', 'previous_institution',
            'previous_marks'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'guardian_address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['program'].queryset = DepartmentProgram.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['program'].queryset = DepartmentProgram.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['program'].queryset = self.instance.department.programs.all()

class StudentEnrollmentForm(forms.ModelForm):
    class Meta:
        model = StudentEnrollment
        fields = ['program', 'semester', 'academic_year']
        widgets = {
            'academic_year': forms.TextInput(attrs={'placeholder': 'e.g., 2023-2024'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['program'].queryset = DepartmentProgram.objects.all() 