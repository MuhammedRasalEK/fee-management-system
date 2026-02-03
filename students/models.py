from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admission_no = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    semester = models.IntegerField()
    dob = models.DateField()

    def __str__(self):
        return self.user.username

class Fee(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=62225)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def balance_amount(self):
        return self.total_amount - self.paid_amount

class Payment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)