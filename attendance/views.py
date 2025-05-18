from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from .models import Attendance
from .forms import AttendanceForm, AttendanceFilterForm
from students.models import Student
from courses.models import Course
from faculty.models import Faculty
from departments.models import Department
from django.utils import timezone

def is_faculty(user):
    return user.groups.filter(name='Faculty').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(is_faculty)
def faculty_attendance(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    attendances = Attendance.objects.filter(recorded_by=faculty)
    return render(request, 'attendance/faculty_attendance.html', {
        'faculty': faculty,
        'attendances': attendances
    })

@login_required
@user_passes_test(is_faculty)
def take_attendance(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.recorded_by = faculty
            attendance.save()
            messages.success(request, 'Attendance recorded successfully.')
            return redirect('attendance:faculty_attendance', pk=faculty.pk)
    else:
        form = AttendanceForm()
    return render(request, 'attendance/take_attendance.html', {
        'faculty': faculty,
        'form': form
    })

@login_required
@user_passes_test(is_faculty)
def edit_attendance(request, pk, attendance_pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    attendance = get_object_or_404(Attendance, pk=attendance_pk, recorded_by=faculty)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance updated successfully.')
            return redirect('attendance:faculty_attendance', pk=faculty.pk)
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'attendance/edit_attendance.html', {
        'faculty': faculty,
        'attendance': attendance,
        'form': form
    })

@login_required
def student_attendance(request, pk):
    student = get_object_or_404(Student, pk=pk)
    attendances = Attendance.objects.filter(student=student)
    return render(request, 'attendance/student_attendance.html', {
        'student': student,
        'attendances': attendances
    })

@login_required
def student_course_attendance(request, pk, course_pk):
    student = get_object_or_404(Student, pk=pk)
    course = get_object_or_404(Course, pk=course_pk)
    attendances = Attendance.objects.filter(student=student, course=course)
    return render(request, 'attendance/student_course_attendance.html', {
        'student': student,
        'course': course,
        'attendances': attendances
    })

@login_required
def course_attendance(request, pk):
    course = get_object_or_404(Course, pk=pk)
    attendances = Attendance.objects.filter(course=course)
    return render(request, 'attendance/course_attendance.html', {
        'course': course,
        'attendances': attendances
    })

@login_required
def course_date_attendance(request, pk, date):
    course = get_object_or_404(Course, pk=pk)
    attendances = Attendance.objects.filter(course=course, date=date)
    return render(request, 'attendance/course_date_attendance.html', {
        'course': course,
        'date': date,
        'attendances': attendances
    })

@login_required
@user_passes_test(is_admin)
def department_attendance(request, pk):
    department = get_object_or_404(Department, pk=pk)
    attendances = Attendance.objects.filter(course__department=department)
    return render(request, 'attendance/department_attendance.html', {
        'department': department,
        'attendances': attendances
    })

@login_required
@user_passes_test(is_admin)
def department_date_attendance(request, pk, date):
    department = get_object_or_404(Department, pk=pk)
    attendances = Attendance.objects.filter(course__department=department, date=date)
    return render(request, 'attendance/department_date_attendance.html', {
        'department': department,
        'date': date,
        'attendances': attendances
    })

@login_required
@user_passes_test(is_admin)
def attendance_reports(request):
    if request.method == 'POST':
        form = AttendanceFilterForm(request.POST)
        if form.is_valid():
            # Generate report based on form data
            pass
    else:
        form = AttendanceFilterForm()
    return render(request, 'attendance/reports.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def generate_report(request):
    if request.method == 'POST':
        form = AttendanceFilterForm(request.POST)
        if form.is_valid():
            # Generate and save report
            messages.success(request, 'Report generated successfully.')
            return redirect('attendance:reports')
    return redirect('attendance:reports')

@login_required
@user_passes_test(is_admin)
def download_report(request, report_pk):
    # Implement report download logic
    pass

# Create your views here.
