from django.db import models
from django.utils import timezone

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey('faculty.Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')
    established_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']

class DepartmentProgram(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    duration = models.PositiveIntegerField(help_text="Duration in years")
    total_credits = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    coordinator = models.ForeignKey('faculty.Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='coordinated_programs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        unique_together = ['department', 'code']
        ordering = ['name']
