from django.urls import path
from . import views

app_name = 'faculty'

urlpatterns = [
    # Faculty list and detail views
    path('', views.faculty_list, name='faculty_list'),
    path('create/', views.faculty_create, name='faculty_create'),
    path('<int:pk>/', views.faculty_detail, name='faculty_detail'),
    path('<int:pk>/edit/', views.faculty_edit, name='faculty_edit'),
    path('<int:pk>/delete/', views.faculty_delete, name='faculty_delete'),
    
    # Faculty course management
    path('<int:pk>/courses/', views.faculty_courses, name='faculty_courses'),
    path('<int:pk>/courses/assign/', views.assign_course, name='assign_course'),
    path('<int:pk>/courses/<int:course_pk>/remove/', views.remove_course, name='remove_course'),
    
    # Faculty attendance management
    path('<int:pk>/attendance/', views.faculty_attendance, name='faculty_attendance'),
    path('<int:pk>/attendance/take/', views.take_attendance, name='take_attendance'),
    path('<int:pk>/attendance/<int:attendance_pk>/edit/', views.edit_attendance, name='edit_attendance'),
    
    # Faculty grade management
    path('<int:pk>/grades/', views.faculty_grades, name='faculty_grades'),
    path('<int:pk>/grades/assign/', views.assign_grade, name='assign_grade'),
    path('<int:pk>/grades/<int:grade_pk>/edit/', views.edit_grade, name='edit_grade'),
    
    # Faculty timetable
    path('<int:pk>/timetable/', views.faculty_timetable, name='faculty_timetable'),
    
    # Faculty exams
    path('<int:pk>/exams/', views.faculty_exams, name='faculty_exams'),
    path('<int:pk>/exams/create/', views.create_exam, name='create_exam'),
    path('<int:pk>/exams/<int:exam_pk>/edit/', views.edit_exam, name='edit_exam'),
] 