from django.db import models
from students.models import Student
from courses.models import Course
from faculty.models import Faculty

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='recorded_attendances')

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date}"

    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date', 'student__roll_number']
