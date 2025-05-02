from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Count, Sum
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from .models import *
from .forms import *
import json
from datetime import datetime

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_faculty(user):
    return user.groups.filter(name='Faculty').exists()

def is_student(user):
    return user.groups.filter(name='Student').exists()

@login_required
def dashboard(request):
    if is_admin(request.user):
        return admin_dashboard(request)
    elif is_faculty(request.user):
        return faculty_dashboard(request)
    elif is_student(request.user):
        return student_dashboard(request)
    return redirect('login')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_faculty = Faculty.objects.count()
    total_courses = Course.objects.count()
    total_departments = Department.objects.count()
    
    recent_notifications = Notification.objects.filter(
        target_users=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_courses': total_courses,
        'total_departments': total_departments,
        'recent_notifications': recent_notifications,
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
@user_passes_test(is_faculty)
def faculty_dashboard(request):
    faculty = request.user.faculty
    courses = CourseAssignment.objects.filter(faculty=faculty)
    recent_attendances = Attendance.objects.filter(
        recorded_by=faculty
    ).order_by('-date')[:5]
    
    context = {
        'faculty': faculty,
        'courses': courses,
        'recent_attendances': recent_attendances,
    }
    return render(request, 'core/faculty_dashboard.html', context)

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student = request.user.student
    enrollments = Enrollment.objects.filter(student=student, is_active=True)
    recent_attendances = Attendance.objects.filter(
        student=student
    ).order_by('-date')[:5]
    recent_grades = Grade.objects.filter(
        enrollment__student=student
    ).order_by('-created_at')[:5]
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'recent_attendances': recent_attendances,
        'recent_grades': recent_grades,
    }
    return render(request, 'core/student_dashboard.html', context)

# Department Management
@login_required
@user_passes_test(is_admin)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'core/department_list.html', {'departments': departments})

@login_required
@user_passes_test(is_admin)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'core/department_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'core/department_form.html', {'form': form, 'department': department})

# Program Management
@login_required
@user_passes_test(is_admin)
def program_list(request):
    programs = Program.objects.all()
    return render(request, 'core/program_list.html', {'programs': programs})

@login_required
@user_passes_test(is_admin)
def program_create(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program created successfully.')
            return redirect('program_list')
    else:
        form = ProgramForm()
    return render(request, 'core/program_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def program_edit(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program updated successfully.')
            return redirect('program_list')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'core/program_form.html', {'form': form, 'program': program})

# Course Management
@login_required
@user_passes_test(is_admin)
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})

@login_required
@user_passes_test(is_admin)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'core/course_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'core/course_form.html', {'form': form, 'course': course})

# Faculty Management
@login_required
@user_passes_test(is_admin)
def faculty_list(request):
    faculty = Faculty.objects.all()
    return render(request, 'core/faculty_list.html', {'faculty': faculty})

@login_required
@user_passes_test(is_admin)
def faculty_create(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        faculty_form = FacultyForm(request.POST)
        if user_form.is_valid() and faculty_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                faculty = faculty_form.save(commit=False)
                faculty.user = user
                faculty.save()
                user.groups.add(Group.objects.get(name='Faculty'))
            messages.success(request, 'Faculty member created successfully.')
            return redirect('faculty_list')
    else:
        user_form = UserRegistrationForm()
        faculty_form = FacultyForm()
    return render(request, 'core/faculty_form.html', {
        'user_form': user_form,
        'faculty_form': faculty_form
    })

@login_required
@user_passes_test(is_admin)
def faculty_edit(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, instance=faculty.user)
        faculty_form = FacultyForm(request.POST, instance=faculty)
        if user_form.is_valid() and faculty_form.is_valid():
            with transaction.atomic():
                user_form.save()
                faculty_form.save()
            messages.success(request, 'Faculty member updated successfully.')
            return redirect('faculty_list')
    else:
        user_form = UserRegistrationForm(instance=faculty.user)
        faculty_form = FacultyForm(instance=faculty)
    return render(request, 'core/faculty_form.html', {
        'user_form': user_form,
        'faculty_form': faculty_form,
        'faculty': faculty
    })

# Student Management
@login_required
@user_passes_test(is_admin)
def student_list(request):
    students = Student.objects.all()
    return render(request, 'core/student_list.html', {'students': students})

@login_required
@user_passes_test(is_admin)
def student_create(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                student = student_form.save(commit=False)
                student.user = user
                student.save()
                user.groups.add(Group.objects.get(name='Student'))
            messages.success(request, 'Student created successfully.')
            return redirect('student_list')
    else:
        user_form = UserRegistrationForm()
        student_form = StudentForm()
    return render(request, 'core/student_form.html', {
        'user_form': user_form,
        'student_form': student_form
    })

@login_required
@user_passes_test(is_admin)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, instance=student.user)
        student_form = StudentForm(request.POST, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            with transaction.atomic():
                user_form.save()
                student_form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
    else:
        user_form = UserRegistrationForm(instance=student.user)
        student_form = StudentForm(instance=student)
    return render(request, 'core/student_form.html', {
        'user_form': user_form,
        'student_form': student_form,
        'student': student
    })

# Course Assignment
@login_required
@user_passes_test(is_admin)
def course_assignment_list(request):
    assignments = CourseAssignment.objects.all()
    return render(request, 'core/course_assignment_list.html', {'assignments': assignments})

@login_required
@user_passes_test(is_admin)
def course_assignment_create(request):
    if request.method == 'POST':
        form = CourseAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course assigned successfully.')
            return redirect('course_assignment_list')
    else:
        form = CourseAssignmentForm()
    return render(request, 'core/course_assignment_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def course_assignment_edit(request, pk):
    assignment = get_object_or_404(CourseAssignment, pk=pk)
    if request.method == 'POST':
        form = CourseAssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course assignment updated successfully.')
            return redirect('course_assignment_list')
    else:
        form = CourseAssignmentForm(instance=assignment)
    return render(request, 'core/course_assignment_form.html', {'form': form, 'assignment': assignment})

# Enrollment Management
@login_required
@user_passes_test(is_admin)
def enrollment_list(request):
    enrollments = Enrollment.objects.all()
    return render(request, 'core/enrollment_list.html', {'enrollments': enrollments})

@login_required
@user_passes_test(is_admin)
def enrollment_create(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student enrolled successfully.')
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm()
    return render(request, 'core/enrollment_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def enrollment_edit(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enrollment updated successfully.')
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm(instance=enrollment)
    return render(request, 'core/enrollment_form.html', {'form': form, 'enrollment': enrollment})

# Attendance Management
@login_required
@user_passes_test(is_faculty)
def attendance_list(request):
    form = AttendanceFilterForm(request.GET or None)
    attendances = Attendance.objects.filter(recorded_by=request.user.faculty)
    
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
    
    return render(request, 'core/attendance_list.html', {
        'attendances': attendances,
        'form': form
    })

@login_required
@user_passes_test(is_faculty)
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.recorded_by = request.user.faculty
            attendance.save()
            messages.success(request, 'Attendance recorded successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'core/attendance_form.html', {'form': form})

@login_required
@user_passes_test(is_faculty)
def attendance_edit(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if attendance.recorded_by != request.user.faculty:
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
    return render(request, 'core/attendance_form.html', {'form': form, 'attendance': attendance})

# Grade Management
@login_required
@user_passes_test(is_faculty)
def grade_list(request):
    form = GradeFilterForm(request.GET or None)
    grades = Grade.objects.filter(assigned_by=request.user.faculty)
    
    if form.is_valid():
        course = form.cleaned_data.get('course')
        semester = form.cleaned_data.get('semester')
        academic_year = form.cleaned_data.get('academic_year')
        
        if course:
            grades = grades.filter(enrollment__course=course)
        if semester:
            grades = grades.filter(enrollment__semester=semester)
        if academic_year:
            grades = grades.filter(enrollment__academic_year=academic_year)
    
    return render(request, 'core/grade_list.html', {
        'grades': grades,
        'form': form
    })

@login_required
@user_passes_test(is_faculty)
def grade_create(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.assigned_by = request.user.faculty
            grade.save()
            messages.success(request, 'Grade assigned successfully.')
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'core/grade_form.html', {'form': form})

@login_required
@user_passes_test(is_faculty)
def grade_edit(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if grade.assigned_by != request.user.faculty:
        messages.error(request, 'You do not have permission to edit this grade.')
        return redirect('grade_list')
    
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade updated successfully.')
            return redirect('grade_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'core/grade_form.html', {'form': form, 'grade': grade})

# Fee Management
@login_required
@user_passes_test(is_admin)
def fee_structure_list(request):
    fee_structures = FeeStructure.objects.all()
    return render(request, 'core/fee_structure_list.html', {'fee_structures': fee_structures})

@login_required
@user_passes_test(is_admin)
def fee_structure_create(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure created successfully.')
            return redirect('fee_structure_list')
    else:
        form = FeeStructureForm()
    return render(request, 'core/fee_structure_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def fee_structure_edit(request, pk):
    fee_structure = get_object_or_404(FeeStructure, pk=pk)
    if request.method == 'POST':
        form = FeeStructureForm(request.POST, instance=fee_structure)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure updated successfully.')
            return redirect('fee_structure_list')
    else:
        form = FeeStructureForm(instance=fee_structure)
    return render(request, 'core/fee_structure_form.html', {'form': form, 'fee_structure': fee_structure})

@login_required
@user_passes_test(is_admin)
def fee_payment_list(request):
    form = FeeFilterForm(request.GET or None)
    payments = FeePayment.objects.all()
    
    if form.is_valid():
        program = form.cleaned_data.get('program')
        semester = form.cleaned_data.get('semester')
        academic_year = form.cleaned_data.get('academic_year')
        payment_status = form.cleaned_data.get('payment_status')
        
        if program:
            payments = payments.filter(fee_structure__program=program)
        if semester:
            payments = payments.filter(fee_structure__semester=semester)
        if academic_year:
            payments = payments.filter(fee_structure__academic_year=academic_year)
        if payment_status:
            if payment_status == 'paid':
                payments = payments.filter(amount_paid__gte=F('fee_structure__total_fee'))
            else:
                payments = payments.filter(amount_paid__lt=F('fee_structure__total_fee'))
    
    return render(request, 'core/fee_payment_list.html', {
        'payments': payments,
        'form': form
    })

@login_required
@user_passes_test(is_admin)
def fee_payment_create(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee payment recorded successfully.')
            return redirect('fee_payment_list')
    else:
        form = FeePaymentForm()
    return render(request, 'core/fee_payment_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def fee_payment_edit(request, pk):
    payment = get_object_or_404(FeePayment, pk=pk)
    if request.method == 'POST':
        form = FeePaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee payment updated successfully.')
            return redirect('fee_payment_list')
    else:
        form = FeePaymentForm(instance=payment)
    return render(request, 'core/fee_payment_form.html', {'form': form, 'payment': payment})

# Timetable Management
@login_required
@user_passes_test(is_admin)
def timetable_list(request):
    timetables = Timetable.objects.all()
    return render(request, 'core/timetable_list.html', {'timetables': timetables})

@login_required
@user_passes_test(is_admin)
def timetable_create(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timetable entry created successfully.')
            return redirect('timetable_list')
    else:
        form = TimetableForm()
    return render(request, 'core/timetable_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def timetable_edit(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timetable entry updated successfully.')
            return redirect('timetable_list')
    else:
        form = TimetableForm(instance=timetable)
    return render(request, 'core/timetable_form.html', {'form': form, 'timetable': timetable})

# Exam Management
@login_required
@user_passes_test(is_admin)
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'core/exam_list.html', {'exams': exams})

@login_required
@user_passes_test(is_admin)
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = request.user.faculty
            exam.save()
            messages.success(request, 'Exam created successfully.')
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'core/exam_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam updated successfully.')
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'core/exam_form.html', {'form': form, 'exam': exam})

# Notification Management
@login_required
@user_passes_test(is_admin)
def notification_list(request):
    notifications = Notification.objects.filter(created_by=request.user)
    return render(request, 'core/notification_list.html', {'notifications': notifications})

@login_required
@user_passes_test(is_admin)
def notification_create(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.created_by = request.user
            notification.save()
            form.save_m2m()  # Save the many-to-many relationships
            messages.success(request, 'Notification created successfully.')
            return redirect('notification_list')
    else:
        form = NotificationForm()
    return render(request, 'core/notification_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def notification_edit(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    if notification.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this notification.')
        return redirect('notification_list')
    
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification updated successfully.')
            return redirect('notification_list')
    else:
        form = NotificationForm(instance=notification)
    return render(request, 'core/notification_form.html', {'form': form, 'notification': notification})

# Report Generation
@login_required
@user_passes_test(is_admin)
def report_list(request):
    reports = Report.objects.filter(generated_by=request.user)
    return render(request, 'core/report_list.html', {'reports': reports})

@login_required
@user_passes_test(is_admin)
def generate_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.generated_by = request.user
            report.save()
            messages.success(request, 'Report generated successfully.')
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'core/report_form.html', {'form': form})

# Student Views
@login_required
@user_passes_test(is_student)
def student_attendance_view(request):
    student = request.user.student
    form = AttendanceFilterForm(request.GET or None)
    attendances = Attendance.objects.filter(student=student)
    
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
    
    return render(request, 'core/student_attendance.html', {
        'attendances': attendances,
        'form': form
    })

@login_required
@user_passes_test(is_student)
def student_grades_view(request):
    student = request.user.student
    form = GradeFilterForm(request.GET or None)
    grades = Grade.objects.filter(enrollment__student=student)
    
    if form.is_valid():
        course = form.cleaned_data.get('course')
        semester = form.cleaned_data.get('semester')
        academic_year = form.cleaned_data.get('academic_year')
        
        if course:
            grades = grades.filter(enrollment__course=course)
        if semester:
            grades = grades.filter(enrollment__semester=semester)
        if academic_year:
            grades = grades.filter(enrollment__academic_year=academic_year)
    
    return render(request, 'core/student_grades.html', {
        'grades': grades,
        'form': form
    })

@login_required
@user_passes_test(is_student)
def student_fees_view(request):
    student = request.user.student
    payments = FeePayment.objects.filter(student=student)
    return render(request, 'core/student_fees.html', {'payments': payments})

@login_required
@user_passes_test(is_student)
def student_timetable_view(request):
    student = request.user.student
    enrollments = Enrollment.objects.filter(student=student, is_active=True)
    courses = [enrollment.course for enrollment in enrollments]
    timetables = Timetable.objects.filter(course__in=courses)
    return render(request, 'core/student_timetable.html', {'timetables': timetables})

@login_required
@user_passes_test(is_student)
def student_exams_view(request):
    student = request.user.student
    enrollments = Enrollment.objects.filter(student=student, is_active=True)
    courses = [enrollment.course for enrollment in enrollments]
    exams = Exam.objects.filter(course__in=courses)
    return render(request, 'core/student_exams.html', {'exams': exams})

# Faculty Views
@login_required
@user_passes_test(is_faculty)
def faculty_courses_view(request):
    faculty = request.user.faculty
    assignments = CourseAssignment.objects.filter(faculty=faculty)
    return render(request, 'core/faculty_courses.html', {'assignments': assignments})

@login_required
@user_passes_test(is_faculty)
def faculty_students_view(request):
    faculty = request.user.faculty
    assignments = CourseAssignment.objects.filter(faculty=faculty)
    courses = [assignment.course for assignment in assignments]
    enrollments = Enrollment.objects.filter(course__in=courses, is_active=True)
    students = [enrollment.student for enrollment in enrollments]
    return render(request, 'core/faculty_students.html', {'students': students})

@login_required
@user_passes_test(is_faculty)
def faculty_timetable_view(request):
    faculty = request.user.faculty
    timetables = Timetable.objects.filter(faculty=faculty)
    return render(request, 'core/faculty_timetable.html', {'timetables': timetables})

@login_required
@user_passes_test(is_faculty)
def faculty_exams_view(request):
    faculty = request.user.faculty
    exams = Exam.objects.filter(created_by=faculty)
    return render(request, 'core/faculty_exams.html', {'exams': exams}) 