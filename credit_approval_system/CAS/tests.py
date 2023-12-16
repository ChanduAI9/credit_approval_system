# tests.py
from django.test import TestCase
from .models import Customer, Loan
from .utils import calculate_loan_credit_score, check_loan_eligibility, calculate_approved_limit
from decimal import Decimal

class LoanTestCase(TestCase):
    def setUp(self):
        # Create a customer 
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            monthly_salary=Decimal('5000.00'),
            phone_number='1234567890',
            approved_limit=Decimal('0.00'),
            current_debt=Decimal('0.00')
        )

        # Create a loan 
        self.loan = Loan.objects.create(
            customer=self.customer,
            loan_id='ABC123',
            loan_amount=Decimal('10000.00'),
            tenure=12,
            interest_rate=Decimal('5.0'),
            monthly_repayment=Decimal('0.00'),
            emis_paid_on_time=6,
            start_date='2023-01-01',
            end_date='2023-12-31'
        )

    def test_calculate_loan_credit_score(self):
    
        expected_credit_score = 0.5
        actual_credit_score = calculate_loan_credit_score(self.loan)
        self.assertEqual(expected_credit_score, actual_credit_score)

    def test_check_loan_eligibility(self):
    
        expected_approval = True
        expected_corrected_interest_rate = Decimal('5.0')
        expected_monthly_installment = Decimal('888.89')

       
        actual_approval, actual_corrected_interest_rate, actual_monthly_installment = check_loan_eligibility(
            self.customer, Decimal('10000.00'), Decimal('5.0'), 12
        )

        self.assertEqual(expected_approval, actual_approval)
        self.assertEqual(expected_corrected_interest_rate, actual_corrected_interest_rate)
        self.assertEqual(expected_monthly_installment, actual_monthly_installment)

    def test_calculate_approved_limit(self):
        

        expected_approved_limit = Decimal('180000.00')

     
        actual_approved_limit = calculate_approved_limit(Decimal('5000.00'))

       
        self.assertEqual(expected_approved_limit, actual_approved_limit)
