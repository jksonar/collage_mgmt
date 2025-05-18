from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Faculty attendance views
    path('faculty/<int:pk>/', views.faculty_attendance, name='faculty_attendance'),
    path('faculty/<int:pk>/take/', views.take_attendance, name='take_attendance'),
    path('faculty/<int:pk>/edit/<int:attendance_pk>/', views.edit_attendance, name='edit_attendance'),
    
    # Student attendance views
    path('student/<int:pk>/', views.student_attendance, name='student_attendance'),
    path('student/<int:pk>/course/<int:course_pk>/', views.student_course_attendance, name='student_course_attendance'),
    
    # Course attendance views
    path('course/<int:pk>/', views.course_attendance, name='course_attendance'),
    path('course/<int:pk>/date/<str:date>/', views.course_date_attendance, name='course_date_attendance'),
    
    # Department attendance views
    path('department/<int:pk>/', views.department_attendance, name='department_attendance'),
    path('department/<int:pk>/date/<str:date>/', views.department_date_attendance, name='department_date_attendance'),
    
    # Attendance reports
    path('reports/', views.attendance_reports, name='reports'),
    path('reports/generate/', views.generate_report, name='generate_report'),
    path('reports/download/<int:report_pk>/', views.download_report, name='download_report'),
] 