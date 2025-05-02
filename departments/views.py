from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm

# Create your views here.

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/list.html', {'departments': departments})

@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'departments/detail.html', {'department': department})

@login_required
def department_create(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create departments.')
        return redirect('department_list')
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    
    return render(request, 'departments/form.html', {'form': form, 'title': 'Create Department'})

@login_required
def department_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to update departments.')
        return redirect('department_list')
    
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully.')
            return redirect('department_detail', pk=department.pk)
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'departments/form.html', {'form': form, 'title': 'Update Department'})

@login_required
def department_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete departments.')
        return redirect('department_list')
    
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully.')
        return redirect('department_list')
    
    return render(request, 'departments/confirm_delete.html', {'department': department})
