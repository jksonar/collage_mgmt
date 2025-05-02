from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from .forms import CourseForm

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/list.html', {'courses': courses})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/detail.html', {'course': course})

@login_required
def course_create(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create courses.')
        return redirect('course_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()
    
    return render(request, 'courses/form.html', {'form': form, 'title': 'Create Course'})

@login_required
def course_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to update courses.')
        return redirect('course_list')
    
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/form.html', {'form': form, 'title': 'Update Course'})

@login_required
def course_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete courses.')
        return redirect('course_list')
    
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('course_list')
    
    return render(request, 'courses/confirm_delete.html', {'course': course})
