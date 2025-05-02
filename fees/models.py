from django.db import models
from students.models import Student
from courses.models import Course

class FeeStructure(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2)
    laboratory_fee = models.DecimalField(max_digits=10, decimal_places=2)
    examination_fee = models.DecimalField(max_digits=10, decimal_places=2)
    other_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    late_fee_penalty = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.course.name} - {self.semester} {self.academic_year}"

    class Meta:
        unique_together = ['course', 'semester', 'academic_year']

class FeePayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('BANK', 'Bank Transfer'),
        ('UPI', 'UPI'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    is_late_payment = models.BooleanField(default=False)
    late_fee_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.fee_structure}"

    class Meta:
        ordering = ['-payment_date'] 