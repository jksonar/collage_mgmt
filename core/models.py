from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True, related_name='department_head')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Program(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    duration_years = models.PositiveIntegerField()
    total_credits = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    credits = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    syllabus = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty_members')
    designation = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    joining_date = models.DateField()
    phone = models.CharField(max_length=15)
    office_location = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='students')
    admission_date = models.DateField()
    graduation_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"

class CourseAssignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='course_assignments')
    semester = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=9)  # Format: YYYY-YYYY
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('course', 'faculty', 'semester', 'academic_year')

    def __str__(self):
        return f"{self.course} - {self.faculty} ({self.semester} - {self.academic_year})"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=9)
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course', 'semester', 'academic_year')

    def __str__(self):
        return f"{self.student} - {self.course} ({self.semester} - {self.academic_year})"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='recorded_attendances')
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='verified_attendances')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student} - {self.course} ({self.date})"

class Grade(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('F', 'F'),
    ]

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grades')
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    remarks = models.TextField(blank=True)
    assigned_by = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='assigned_grades')
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='verified_grades')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.enrollment} - {self.grade}"

class FeeStructure(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='fee_structures')
    semester = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=9)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2)
    lab_fee = models.DecimalField(max_digits=10, decimal_places=2)
    other_fee = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('program', 'semester', 'academic_year')

    def __str__(self):
        return f"{self.program} - Semester {self.semester} ({self.academic_year})"

    @property
    def total_fee(self):
        return sum([
            self.tuition_fee,
            self.registration_fee,
            self.library_fee,
            self.lab_fee,
            self.other_fee
        ])

class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.receipt_number}"

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

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetable_entries')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='timetable_entries')
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.CharField(max_length=50)
    semester = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=9)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('course', 'day', 'start_time', 'semester', 'academic_year')

    def __str__(self):
        return f"{self.course} - {self.day} {self.start_time}-{self.end_time}"

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    exam_type = models.CharField(max_length=50)  # e.g., Midterm, Final, Quiz
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
    classroom = models.CharField(max_length=50)
    semester = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=9)
    created_by = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='created_exams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course} - {self.exam_type} ({self.date})"

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50)  # e.g., Admission, Exam, Result
    target_users = models.ManyToManyField(User, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('STUDENT_LIST', 'Student List'),
        ('FACULTY_LIST', 'Faculty List'),
        ('COURSE_LIST', 'Course List'),
        ('ATTENDANCE_SUMMARY', 'Attendance Summary'),
        ('GRADE_REPORT', 'Grade Report'),
        ('FEE_REPORT', 'Fee Report'),
    ]

    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    parameters = models.JSONField()  # Store report filters and parameters
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_reports')
    file_path = models.FileField(upload_to='reports/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.created_at}" 