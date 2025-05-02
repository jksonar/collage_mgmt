from django.db import models
from django.contrib.auth.models import User
from departments.models import Department
from courses.models import Course

class Admission(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    merit_rank = models.PositiveIntegerField(null=True, blank=True)
    previous_qualification = models.CharField(max_length=200)
    previous_institution = models.CharField(max_length=200)
    previous_marks = models.DecimalField(max_digits=5, decimal_places=2)
    entrance_exam_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    interview_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course.name}"

    class Meta:
        ordering = ['-application_date'] 