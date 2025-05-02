from django.db import models
from students.models import Student
from courses.models import Course
from faculty.models import Faculty

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
        ('D', 'D'),
        ('F', 'F'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='grades')
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)  # e.g., "2023-2024"
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    remarks = models.TextField(blank=True)
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course} - {self.grade}"

    class Meta:
        unique_together = ['student', 'course', 'semester', 'academic_year']
        ordering = ['-academic_year', 'semester', 'student__roll_number']
