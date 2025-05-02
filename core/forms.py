from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Department, Program, Course, Faculty, Student,
    CourseAssignment, Enrollment, Attendance, Grade,
    FeeStructure, FeePayment, Timetable, Exam,
    Notification, Report
)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'code', 'department', 'duration_years', 'total_credits', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'department', 'credits', 'description', 'syllabus']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'syllabus': forms.Textarea(attrs={'rows': 5}),
        }

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['department', 'designation', 'specialization', 'joining_date', 'phone', 'office_location']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'department', 'program', 'admission_date', 'graduation_date', 'phone', 'address']
        widgets = {
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'graduation_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class CourseAssignmentForm(forms.ModelForm):
    class Meta:
        model = CourseAssignment
        fields = ['course', 'faculty', 'semester', 'academic_year']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'semester', 'academic_year']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['enrollment', 'grade', 'marks', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['program', 'semester', 'academic_year', 'tuition_fee', 'registration_fee',
                 'library_fee', 'lab_fee', 'other_fee']

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['student', 'fee_structure', 'amount_paid', 'payment_date', 'payment_method',
                 'transaction_id', 'remarks']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['course', 'faculty', 'day', 'start_time', 'end_time', 'classroom',
                 'semester', 'academic_year']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'exam_type', 'date', 'start_time', 'end_time', 'total_marks',
                 'passing_marks', 'classroom', 'semester', 'academic_year']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'message', 'notification_type', 'target_users']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
            'target_users': forms.SelectMultiple(attrs={'class': 'select2'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'parameters']
        widgets = {
            'parameters': forms.HiddenInput(),
        }

class AttendanceFilterForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(choices=Attendance.STATUS_CHOICES, required=False)

class GradeFilterForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False)
    semester = forms.IntegerField(required=False)
    academic_year = forms.CharField(max_length=9, required=False)

class FeeFilterForm(forms.Form):
    program = forms.ModelChoiceField(queryset=Program.objects.all(), required=False)
    semester = forms.IntegerField(required=False)
    academic_year = forms.CharField(max_length=9, required=False)
    payment_status = forms.ChoiceField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], required=False) 