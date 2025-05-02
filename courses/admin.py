from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'credits', 'duration', 'is_active')
    search_fields = ('name', 'code', 'department__name')
    list_filter = ('department', 'is_active', 'credits')
    filter_horizontal = ('prerequisites',)
