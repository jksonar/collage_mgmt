from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('STUDENT', 'Student Report'),
        ('FACULTY', 'Faculty Report'),
        ('COURSE', 'Course Report'),
        ('ATTENDANCE', 'Attendance Report'),
        ('EXAM', 'Exam Report'),
        ('FEE', 'Fee Report'),
        ('ADMISSION', 'Admission Report'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    parameters = models.JSONField(default=dict)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(default=timezone.now)
    file_path = models.FileField(upload_to='reports/', blank=True)
    is_archived = models.BooleanField(default=False)
    archive_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.title}"

    def archive(self):
        if not self.is_archived:
            self.is_archived = True
            self.archive_date = timezone.now()
            self.save()

    class Meta:
        ordering = ['-generated_at'] 