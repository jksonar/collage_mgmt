from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_of_department', 'contact_email', 'contact_phone')
    search_fields = ('name', 'code', 'head_of_department')
    list_filter = ('established_date',)
