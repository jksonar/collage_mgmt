from django.db import models
from departments.models import Department, DepartmentProgram
from django.utils import timezone

class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('CORE', 'Core'),
        ('ELECTIVE', 'Elective'),
        ('GENERAL', 'General'),
        ('LAB', 'Laboratory'),
        ('PROJECT', 'Project'),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    program = models.ForeignKey(DepartmentProgram, on_delete=models.CASCADE)
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES)
    credits = models.PositiveIntegerField()
    duration = models.PositiveIntegerField(help_text="Duration in weeks")
    description = models.TextField()
    objectives = models.TextField(blank=True)
    outcomes = models.TextField(blank=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='postrequisites')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['code']

class CourseOffering(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    start_date = models.DateField()
    end_date = models.DateField()
    max_students = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.name} - {self.semester} {self.academic_year}"

    class Meta:
        unique_together = ['course', 'semester', 'academic_year']
        ordering = ['-academic_year', 'semester', 'course__code']
