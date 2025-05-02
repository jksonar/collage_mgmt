from django.contrib import admin
from .models import Faculty

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'designation', 'specialization', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'employee_id', 'department__name')
    list_filter = ('department', 'designation', 'is_active')
    raw_id_fields = ('user',)
