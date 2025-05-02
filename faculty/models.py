from django.db import models
from django.contrib.auth.models import User
from departments.models import Department

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

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

    class Meta:
        verbose_name_plural = "Faculty"
        ordering = ['user__first_name']
