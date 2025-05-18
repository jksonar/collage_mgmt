from django.db import models
from courses.models import Course
from faculty.models import Faculty
from timetable.models import Classroom
from django.utils import timezone

class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('MID', 'Mid-term'),
        ('FINAL', 'Final'),
        ('QUIZ', 'Quiz'),
        ('ASSIGN', 'Assignment'),
        ('PRACTICAL', 'Practical'),
        ('PROJECT', 'Project'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
    instructions = models.TextField(blank=True)
    created_by = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='created_exams')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.name} - {self.get_exam_type_display()} - {self.exam_date}"

    class Meta:
        unique_together = ['course', 'exam_type', 'semester', 'academic_year']
        ordering = ['-exam_date', 'start_time']

class ExamSchedule(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.exam} - {self.date} {self.start_time}-{self.end_time}"

    class Meta:
        unique_together = ['classroom', 'date', 'start_time']
        ordering = ['date', 'start_time']

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)
    evaluated_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    evaluated_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='verified_results')
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam} - {self.marks_obtained}"

    class Meta:
        unique_together = ['exam', 'student']
        ordering = ['-evaluated_at'] 