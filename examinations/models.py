from django.db import models
from courses.models import Course
from students.models import Student
from faculty.models import Faculty
from timetable.models import Classroom

class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('MID', 'Mid-term'),
        ('FINAL', 'Final'),
        ('QUIZ', 'Quiz'),
        ('ASSIGN', 'Assignment'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=5, choices=EXAM_TYPE_CHOICES)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.name} - {self.get_exam_type_display()} - {self.exam_date}"

    class Meta:
        ordering = ['-exam_date']

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    is_pass = models.BooleanField()
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    recorded_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam}"

    class Meta:
        unique_together = ['exam', 'student']
        ordering = ['-recorded_date'] 