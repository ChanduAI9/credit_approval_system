from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Calculate approved_limit using COMPOUND INTEREST SCHEME
        self.approved_limit = round(36 * self.monthly_salary, -5)
        super().save(*args, **kwargs)

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.CharField(max_length=50)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Adjusted scale to 2
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()