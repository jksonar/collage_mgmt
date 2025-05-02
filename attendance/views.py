from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from .models import Attendance
from .forms import AttendanceForm, AttendanceFilterForm
from students.models import Student
from courses.models import Course
from faculty.models import Faculty

def is_faculty(user):
    return user.profile.is_faculty

def is_admin(user):
    return user.profile.is_admin

@login_required
@user_passes_test(lambda u: u.profile.is_faculty or u.profile.is_admin)
def attendance_list(request):
    form = AttendanceFilterForm(request.GET or None)
    attendances = Attendance.objects.all()

    if form.is_valid():
        course = form.cleaned_data.get('course')
        date = form.cleaned_data.get('date')
        status = form.cleaned_data.get('status')

        if course:
            attendances = attendances.filter(course=course)
        if date:
            attendances = attendances.filter(date=date)
        if status:
            attendances = attendances.filter(status=status)

    if request.user.profile.is_faculty:
        faculty = request.user.faculty
        attendances = attendances.filter(recorded_by=faculty)

    return render(request, 'attendance/list.html', {
        'attendances': attendances,
        'form': form
    })

@login_required
@user_passes_test(is_faculty)
def take_attendance(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    faculty = request.user.faculty

    if request.method == 'POST':
        form = AttendanceForm(request.POST, course=course)
        if form.is_valid():
            with transaction.atomic():
                for student in form.cleaned_data['students']:
                    status = form.cleaned_data[f'status_{student.id}']
                    remarks = form.cleaned_data[f'remarks_{student.id}']
                    
                    Attendance.objects.create(
                        student=student,
                        course=course,
                        status=status,
                        remarks=remarks,
                        recorded_by=faculty
                    )
            messages.success(request, 'Attendance recorded successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm(course=course)

    return render(request, 'attendance/take.html', {
        'form': form,
        'course': course
    })

@login_required
@user_passes_test(is_faculty)
def edit_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    
    if request.user.profile.is_faculty and attendance.recorded_by != request.user.faculty:
        messages.error(request, 'You do not have permission to edit this attendance.')
        return redirect('attendance_list')

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance updated successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'attendance/edit.html', {
        'form': form,
        'attendance': attendance
    })

@login_required
@user_passes_test(is_faculty)
def verify_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    faculty = request.user.faculty

    if attendance.is_verified:
        messages.warning(request, 'This attendance is already verified.')
    else:
        attendance.verify(faculty)
        messages.success(request, 'Attendance verified successfully.')

    return redirect('attendance_list')

@login_required
def student_attendance(request):
    if not request.user.profile.is_student:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('home')

    student = request.user.student
    attendances = Attendance.objects.filter(student=student)
    
    form = AttendanceFilterForm(request.GET or None)
    if form.is_valid():
        course = form.cleaned_data.get('course')
        date = form.cleaned_data.get('date')
        status = form.cleaned_data.get('status')

        if course:
            attendances = attendances.filter(course=course)
        if date:
            attendances = attendances.filter(date=date)
        if status:
            attendances = attendances.filter(status=status)

    return render(request, 'attendance/student_list.html', {
        'attendances': attendances,
        'form': form
    })

# Create your views here.
