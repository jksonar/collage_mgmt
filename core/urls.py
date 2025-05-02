from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    # Department Management
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_edit, name='department_edit'),

    # Program Management
    path('programs/', views.program_list, name='program_list'),
    path('programs/create/', views.program_create, name='program_create'),
    path('programs/<int:pk>/edit/', views.program_edit, name='program_edit'),

    # Course Management
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),

    # Faculty Management
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/create/', views.faculty_create, name='faculty_create'),
    path('faculty/<int:pk>/edit/', views.faculty_edit, name='faculty_edit'),

    # Student Management
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),

    # Course Assignment
    path('course-assignments/', views.course_assignment_list, name='course_assignment_list'),
    path('course-assignments/create/', views.course_assignment_create, name='course_assignment_create'),
    path('course-assignments/<int:pk>/edit/', views.course_assignment_edit, name='course_assignment_edit'),

    # Enrollment Management
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/create/', views.enrollment_create, name='enrollment_create'),
    path('enrollments/<int:pk>/edit/', views.enrollment_edit, name='enrollment_edit'),

    # Attendance Management
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/<int:pk>/edit/', views.attendance_edit, name='attendance_edit'),

    # Grade Management
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/create/', views.grade_create, name='grade_create'),
    path('grades/<int:pk>/edit/', views.grade_edit, name='grade_edit'),

    # Fee Management
    path('fee-structures/', views.fee_structure_list, name='fee_structure_list'),
    path('fee-structures/create/', views.fee_structure_create, name='fee_structure_create'),
    path('fee-structures/<int:pk>/edit/', views.fee_structure_edit, name='fee_structure_edit'),
    path('fee-payments/', views.fee_payment_list, name='fee_payment_list'),
    path('fee-payments/create/', views.fee_payment_create, name='fee_payment_create'),
    path('fee-payments/<int:pk>/edit/', views.fee_payment_edit, name='fee_payment_edit'),

    # Timetable Management
    path('timetables/', views.timetable_list, name='timetable_list'),
    path('timetables/create/', views.timetable_create, name='timetable_create'),
    path('timetables/<int:pk>/edit/', views.timetable_edit, name='timetable_edit'),

    # Exam Management
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/create/', views.exam_create, name='exam_create'),
    path('exams/<int:pk>/edit/', views.exam_edit, name='exam_edit'),

    # Notification Management
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/create/', views.notification_create, name='notification_create'),
    path('notifications/<int:pk>/edit/', views.notification_edit, name='notification_edit'),

    # Report Generation
    path('reports/', views.report_list, name='report_list'),
    path('reports/generate/', views.generate_report, name='generate_report'),

    # Student Views
    path('student/attendance/', views.student_attendance_view, name='student_attendance'),
    path('student/grades/', views.student_grades_view, name='student_grades'),
    path('student/fees/', views.student_fees_view, name='student_fees'),
    path('student/timetable/', views.student_timetable_view, name='student_timetable'),
    path('student/exams/', views.student_exams_view, name='student_exams'),

    # Faculty Views
    path('faculty/courses/', views.faculty_courses_view, name='faculty_courses'),
    path('faculty/students/', views.faculty_students_view, name='faculty_students'),
    path('faculty/timetable/', views.faculty_timetable_view, name='faculty_timetable'),
    path('faculty/exams/', views.faculty_exams_view, name='faculty_exams'),
] 