import pandas as pd
from django.core.management.base import BaseCommand
from CAS.models import Customer, Loan

class Command(BaseCommand):
    help = 'Initialize the system with customer and loan data'

    def handle(self, *args, **options):
        customer_excel_path = r'C:\Users\HP\Desktop\Chandu\Assignments\Alemeno\CAS\credit_approval_system\customer_data.xlsx'

        loan_excel_path = r'C:\Users\HP\Desktop\Chandu\Assignments\Alemeno\CAS\credit_approval_system\loan_data.xlsx'

        try:
            customer_data = pd.read_excel(customer_excel_path)

            for index, row in customer_data.iterrows():
                Customer.objects.create(
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    age=row['Age'],
                    monthly_salary=row['Monthly Salary'],
                    phone_number=row['Phone Number']
                )

            self.stdout.write(self.style.SUCCESS('Customer data ingestion completed'))

            loan_data = pd.read_excel(loan_excel_path)

            for index, row in loan_data.iterrows():
                customer_id = row['Customer ID']
                customer = Customer.objects.get(id=customer_id)

                Loan.objects.create(
                    customer=customer,
                    loan_id=row['Loan ID'],
                    loan_amount=row['Loan Amount'],
                    tenure=row['Tenure'],
                    interest_rate=row['Interest Rate'],
                    monthly_repayment=row['Monthly payment'],
                    emis_paid_on_time=row['EMIs paid on Time'],
                    start_date=row['Date of Approval'],
                    end_date=row['End Date']
                )

            self.stdout.write(self.style.SUCCESS('Loan data ingestion completed'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
