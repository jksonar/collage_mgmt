from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Faculty
from .forms import FacultyForm
from courses.models import Course
from attendance.models import Attendance
from grades.models import Grade
from timetable.models import Timetable
from exams.models import Exam

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_faculty(user):
    return user.groups.filter(name='Faculty').exists()

@login_required
@user_passes_test(is_admin)
def faculty_list(request):
    faculties = Faculty.objects.all()
    return render(request, 'faculty/faculty_list.html', {'faculties': faculties})

@login_required
@user_passes_test(is_admin)
def faculty_create(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            faculty = form.save()
            messages.success(request, 'Faculty member created successfully.')
            return redirect('faculty:faculty_detail', pk=faculty.pk)
    else:
        form = FacultyForm()
    return render(request, 'faculty/faculty_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def faculty_detail(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    return render(request, 'faculty/faculty_detail.html', {'faculty': faculty})

@login_required
@user_passes_test(is_admin)
def faculty_edit(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            messages.success(request, 'Faculty member updated successfully.')
            return redirect('faculty:faculty_detail', pk=faculty.pk)
    else:
        form = FacultyForm(instance=faculty)
    return render(request, 'faculty/faculty_form.html', {'form': form, 'faculty': faculty})

@login_required
@user_passes_test(is_admin)
def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        faculty.delete()
        messages.success(request, 'Faculty member deleted successfully.')
        return redirect('faculty:faculty_list')
    return render(request, 'faculty/faculty_confirm_delete.html', {'faculty': faculty})

@login_required
@user_passes_test(is_faculty)
def faculty_courses(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    courses = Course.objects.filter(faculty=faculty)
    return render(request, 'faculty/faculty_courses.html', {'faculty': faculty, 'courses': courses})

@login_required
@user_passes_test(is_admin)
def assign_course(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, pk=course_id)
        course.faculty = faculty
        course.save()
        messages.success(request, 'Course assigned successfully.')
        return redirect('faculty:faculty_courses', pk=faculty.pk)
    available_courses = Course.objects.filter(faculty__isnull=True)
    return render(request, 'faculty/assign_course.html', {'faculty': faculty, 'courses': available_courses})

@login_required
@user_passes_test(is_admin)
def remove_course(request, pk, course_pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    course = get_object_or_404(Course, pk=course_pk)
    if course.faculty == faculty:
        course.faculty = None
        course.save()
        messages.success(request, 'Course removed successfully.')
    return redirect('faculty:faculty_courses', pk=faculty.pk)

@login_required
@user_passes_test(is_faculty)
def faculty_attendance(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    attendances = Attendance.objects.filter(recorded_by=faculty)
    return render(request, 'faculty/faculty_attendance.html', {'faculty': faculty, 'attendances': attendances})

@login_required
@user_passes_test(is_faculty)
def take_attendance(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        # Handle attendance form submission
        pass
    return render(request, 'faculty/take_attendance.html', {'faculty': faculty})

@login_required
@user_passes_test(is_faculty)
def edit_attendance(request, pk, attendance_pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    attendance = get_object_or_404(Attendance, pk=attendance_pk)
    if request.method == 'POST':
        # Handle attendance edit form submission
        pass
    return render(request, 'faculty/edit_attendance.html', {'faculty': faculty, 'attendance': attendance})

@login_required
@user_passes_test(is_faculty)
def faculty_grades(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    grades = Grade.objects.filter(assigned_by=faculty)
    return render(request, 'faculty/faculty_grades.html', {'faculty': faculty, 'grades': grades})

@login_required
@user_passes_test(is_faculty)
def assign_grade(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        # Handle grade assignment form submission
        pass
    return render(request, 'faculty/assign_grade.html', {'faculty': faculty})

@login_required
@user_passes_test(is_faculty)
def edit_grade(request, pk, grade_pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    grade = get_object_or_404(Grade, pk=grade_pk)
    if request.method == 'POST':
        # Handle grade edit form submission
        pass
    return render(request, 'faculty/edit_grade.html', {'faculty': faculty, 'grade': grade})

@login_required
@user_passes_test(is_faculty)
def faculty_timetable(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    timetable = Timetable.objects.filter(faculty=faculty)
    return render(request, 'faculty/faculty_timetable.html', {'faculty': faculty, 'timetable': timetable})

@login_required
@user_passes_test(is_faculty)
def faculty_exams(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    exams = Exam.objects.filter(created_by=faculty)
    return render(request, 'faculty/faculty_exams.html', {'faculty': faculty, 'exams': exams})

@login_required
@user_passes_test(is_faculty)
def create_exam(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        # Handle exam creation form submission
        pass
    return render(request, 'faculty/create_exam.html', {'faculty': faculty})

@login_required
@user_passes_test(is_faculty)
def edit_exam(request, pk, exam_pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    exam = get_object_or_404(Exam, pk=exam_pk)
    if request.method == 'POST':
        # Handle exam edit form submission
        pass
    return render(request, 'faculty/edit_exam.html', {'faculty': faculty, 'exam': exam})
