from django.db import models
from courses.models import Course
from faculty.models import Faculty
from departments.models import Department
from django.utils import timezone

class Classroom(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    building = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    is_laboratory = models.BooleanField(default=False)
    facilities = models.TextField(blank=True)

    def __str__(self):
        return f"{self.building} - {self.room_number}"

    class Meta:
        ordering = ['building', 'room_number']

class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
    ]

    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_break = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_day_display()} {self.start_time} - {self.end_time}"

    class Meta:
        unique_together = ['day', 'start_time', 'end_time']

class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.name} - {self.faculty.user.get_full_name()} - {self.time_slot}"

    class Meta:
        unique_together = ['classroom', 'time_slot', 'semester', 'academic_year']
        ordering = ['time_slot__day', 'time_slot__start_time']

class Timetable(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.name} - {self.get_day_display()} {self.start_time}-{self.end_time}"

    class Meta:
        unique_together = ['classroom', 'day', 'start_time', 'semester', 'academic_year']
        ordering = ['day', 'start_time'] 