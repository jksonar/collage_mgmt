from django.db import models
from django.contrib.auth.models import User
from departments.models import Department, DepartmentProgram
from django.utils import timezone

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    program = models.ForeignKey(DepartmentProgram, on_delete=models.CASCADE)
    admission_date = models.DateField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    phone_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    address = models.TextField()
    nationality = models.CharField(max_length=50)
    religion = models.CharField(max_length=50, blank=True)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_relation = models.CharField(max_length=50, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    guardian_address = models.TextField(blank=True)
    previous_qualification = models.CharField(max_length=100)
    previous_institution = models.CharField(max_length=200)
    previous_marks = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"

    class Meta:
        ordering = ['roll_number']

class StudentEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    program = models.ForeignKey(DepartmentProgram, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    enrollment_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.program.name} - {self.semester} {self.academic_year}"

    class Meta:
        unique_together = ['student', 'program', 'semester', 'academic_year']
        ordering = ['-academic_year', 'semester', 'student__roll_number']
