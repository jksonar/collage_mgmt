from django.db import models
from students.models import Student
from courses.models import Course
from faculty.models import Faculty
from django.utils import timezone

class Transcript(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    total_credits = models.PositiveIntegerField()
    earned_credits = models.PositiveIntegerField()
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.semester} {self.academic_year}"

    def verify(self, faculty):
        if not self.is_verified:
            self.is_verified = True
            self.verified_by = faculty
            self.verified_at = timezone.now()
            self.save()

    class Meta:
        unique_together = ['student', 'semester', 'academic_year']
        ordering = ['-academic_year', 'semester']

class TranscriptCourse(models.Model):
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE, related_name='courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    credits = models.PositiveIntegerField()
    grade_points = models.DecimalField(max_digits=3, decimal_places=2)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.transcript} - {self.course.name}"

    class Meta:
        ordering = ['course__code'] 