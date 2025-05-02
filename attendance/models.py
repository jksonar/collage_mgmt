from django.db import models
from students.models import Student
from courses.models import Course
from faculty.models import Faculty
from django.utils import timezone

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
        ('EXCUSED', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    recorded_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='verified_attendances')
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.name} - {self.date}"

    def verify(self, faculty):
        if not self.is_verified:
            self.is_verified = True
            self.verified_by = faculty
            self.verified_at = timezone.now()
            self.save()

    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date', 'student__user__first_name']
