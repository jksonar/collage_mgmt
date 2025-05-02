from django.db import models
from students.models import Student
from courses.models import Course
from faculty.models import Faculty
from examinations.models import Exam
from django.utils import timezone

class Grade(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('F', 'F'),
        ('I', 'Incomplete'),
        ('W', 'Withdrawn'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='verified_grades')
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.name} - {self.grade}"

    def verify(self, faculty):
        if not self.is_verified:
            self.is_verified = True
            self.verified_by = faculty
            self.verified_at = timezone.now()
            self.save()

    class Meta:
        unique_together = ['student', 'course', 'semester', 'academic_year']
        ordering = ['-recorded_at']
