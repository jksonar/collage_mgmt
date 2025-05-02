from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade', 'semester', 'academic_year', 'marks_obtained', 'total_marks')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__roll_number', 'course__name')
    list_filter = ('grade', 'semester', 'academic_year', 'course', 'faculty')
    date_hierarchy = 'date_recorded'
