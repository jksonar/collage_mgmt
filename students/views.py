from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from .models import Student, StudentEnrollment
from .forms import StudentRegistrationForm, StudentProfileForm, StudentEnrollmentForm
from users.models import UserProfile

def is_student(user):
    return user.profile.is_student

def is_faculty(user):
    return user.profile.is_faculty

def is_admin(user):
    return user.profile.is_admin

@login_required
@user_passes_test(is_admin)
def student_registration(request):
    if request.method == 'POST':
        user_form = StudentRegistrationForm(request.POST)
        if user_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                UserProfile.objects.create(user=user, role='STUDENT')
                messages.success(request, 'Student registered successfully.')
                return redirect('student_profile', user_id=user.id)
    else:
        user_form = StudentRegistrationForm()
    
    return render(request, 'students/registration.html', {'form': user_form})

@login_required
def student_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    student = get_object_or_404(Student, user=user)
    
    if not (request.user.profile.is_admin or request.user == user):
        messages.error(request, 'You do not have permission to view this profile.')
        return redirect('home')
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('student_profile', user_id=user_id)
    else:
        form = StudentProfileForm(instance=student)
    
    enrollments = StudentEnrollment.objects.filter(student=student)
    return render(request, 'students/profile.html', {
        'student': student,
        'form': form,
        'enrollments': enrollments
    })

@login_required
@user_passes_test(is_admin)
def student_enrollment(request, user_id):
    user = get_object_or_404(User, id=user_id)
    student = get_object_or_404(Student, user=user)
    
    if request.method == 'POST':
        form = StudentEnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student
            enrollment.save()
            messages.success(request, 'Student enrolled successfully.')
            return redirect('student_profile', user_id=user_id)
    else:
        form = StudentEnrollmentForm()
    
    return render(request, 'students/enrollment.html', {
        'student': student,
        'form': form
    })

@login_required
def student_list(request):
    if request.user.profile.is_admin:
        students = Student.objects.all()
    elif request.user.profile.is_faculty:
        # Get students enrolled in courses taught by the faculty
        faculty = request.user.faculty
        courses = faculty.courses.all()
        students = Student.objects.filter(enrollments__course__in=courses).distinct()
    else:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('home')
    
    return render(request, 'students/list.html', {'students': students})
