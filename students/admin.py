from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'department', 'course', 'admission_date', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'roll_number', 'department__name')
    list_filter = ('department', 'course', 'gender', 'is_active')
    raw_id_fields = ('user',)
