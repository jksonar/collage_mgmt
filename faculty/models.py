from django.db import models
from django.contrib.auth.models import User
from departments.models import Department
from courses.models import Course
from django.utils import timezone

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty')
    employee_id = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    joining_date = models.DateField()
    qualification = models.CharField(max_length=200)
    experience = models.PositiveIntegerField()  # in years
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id}) - {self.designation}"

    class Meta:
        verbose_name_plural = "Faculty"
        ordering = ['user__first_name']

class FacultyCourseAssignment(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    is_primary_instructor = models.BooleanField(default=True)
    assigned_date = models.DateField(default=timezone.now)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_courses')
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.faculty.user.get_full_name()} - {self.course.name}"

    class Meta:
        unique_together = ['faculty', 'course', 'semester', 'academic_year']
        ordering = ['-academic_year', 'semester', 'faculty__user__first_name']
