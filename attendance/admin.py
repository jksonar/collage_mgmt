from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'faculty')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__roll_number', 'course__name')
    list_filter = ('status', 'date', 'course', 'faculty')
    date_hierarchy = 'date'
