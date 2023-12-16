from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Loan, Customer
from .serializers import LoanSerializer, CustomerSerializer

@api_view(['POST'])
def register_customer(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # Calculate approved_limit 
            monthly_salary = serializer.validated_data['monthly_salary']
            approved_limit = calculate_approved_limit(monthly_salary)

            # Save customer
            customer = serializer.save(approved_limit=approved_limit)

           
            response_data = {
                "customer_id": customer.id,
                "name": f"{customer.first_name} {customer.last_name}",
                "age": customer.age,
                "monthly_salary": customer.monthly_salary,
                "approved_limit": customer.approved_limit,
                "phone_number": customer.phone_number
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def calculate_approved_limit(monthly_salary):
   
    return round(36 * monthly_salary, -5)

@api_view(['POST'])
def check_eligibility(request):
    try:
        
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')

        # Fetch customer
        customer = get_object_or_404(Customer, id=customer_id)

        # Fetch all loans 
        loans = Loan.objects.filter(customer=customer)

        credit_score = calculate_credit_score(loans, customer)
        print(f"Received data: customer_id={customer_id}, loan_amount={loan_amount}, interest_rate={interest_rate}, tenure={tenure}")

        print(f"DEBUG: Interest rate before check: {interest_rate}")

        if interest_rate is None:
            raise ValueError("Interest rate cannot be None")

        try:
            interest_rate = float(interest_rate)
        except (TypeError, ValueError):
            print(f"DEBUG: Conversion to float failed. Interest rate value: {interest_rate}")
            raise ValueError("Invalid interest rate value")

        print(f"DEBUG: Interest rate after check: {interest_rate}")

        approval, corrected_interest_rate = check_loan_eligibility(credit_score, interest_rate)

        print(f"DEBUG: Approval: {approval}")
        print(f"DEBUG: Corrected interest rate: {corrected_interest_rate}")

        monthly_installment = calculate_monthly_installment(float(loan_amount), corrected_interest_rate, int(tenure))

        response_data = {
            "customer_id": customer_id,
            "approval": approval,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_interest_rate,
            "tenure": tenure,
            "monthly_installment": monthly_installment,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as ve:
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def calculate_credit_score(loans, customer):
    total_credit_score = sum([calculate_loan_credit_score(loan) for loan in loans])
    average_credit_score = total_credit_score / max(len(loans), 1)

    print(f"DEBUG: Total Credit Score: {total_credit_score}")
    print(f"DEBUG: Average Credit Score: {average_credit_score}")

    return average_credit_score

def calculate_credit_score(loans, customer):
    total_credit_score = sum([calculate_loan_credit_score(loan) for loan in loans])

    # Avoid division by zero error
    average_credit_score = total_credit_score / max(len(loans), 1)

    return average_credit_score



def check_loan_eligibility(credit_score, interest_rate):
   
    print(f"DEBUG: Credit score: {credit_score}, Interest rate: {interest_rate}")

    
    if credit_score > 50:
        approval = True
        corrected_interest_rate = interest_rate
    elif 50 >= credit_score > 30:
        approval = True
        corrected_interest_rate = max(interest_rate, 12)
    elif 30 >= credit_score > 10:
        approval = True
        corrected_interest_rate = max(interest_rate, 16)
    else:
        approval = False
        corrected_interest_rate = None

    print(f"DEBUG: Approval: {approval}, Corrected interest rate: {corrected_interest_rate}")

    return approval, corrected_interest_rate

def calculate_monthly_installment(loan_amount, interest_rate, tenure):
  

    if interest_rate is None:
        raise ValueError("Interest rate cannot be None")

    if tenure is None or tenure == 0:
        raise ValueError("Tenure must be a non-zero positive integer")

    try:
        interest_rate = float(interest_rate)  #  Decimal or Float
    except (TypeError, ValueError):
        raise ValueError("Invalid interest rate value")

    interest_rate /= 100 

    monthly_rate = interest_rate / 12
    num_installments = tenure * 12
    monthly_installment = (loan_amount * monthly_rate) / (1 - (1 + monthly_rate) ** -num_installments)

    return monthly_installment





@api_view(['POST'])
def create_loan(request):
    try:
    
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')

        customer = Customer.objects.get(id=customer_id)

        eligibility, corrected_interest_rate, monthly_installment = check_loan_eligibility(customer, loan_amount, interest_rate, tenure)

        if eligibility:
            new_loan = Loan.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                interest_rate=corrected_interest_rate,
                tenure=tenure,
                monthly_repayment=monthly_installment
            )

            response_data = {
                "loan_id": new_loan.id,
                "customer_id": customer_id,
                "loan_approved": True,
                "message": "Loan approved",
                "monthly_installment": monthly_installment,
            }

        else:
            response_data = {
                "loan_id": None,
                "customer_id": customer_id,
                "loan_approved": False,
                "message": "Loan not approved",
                "monthly_installment": None,
            }

        return Response(response_data, status=status.HTTP_200_OK)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as ve:
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    





 
def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    if interest_rate is None:
        raise ValueError("Interest rate cannot be None")
    
    if tenure is None or tenure==0:
        raise ValueError("Tenure must be a non-zero positive integer")

    
    if interest_rate is not None:
        monthly_installment = calculate_monthly_installment(float(loan_amount), float(interest_rate), int(tenure))
        return True, float(interest_rate), monthly_installment

    return False, None, None




@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        # loan_id
        loan = get_object_or_404(Loan, id=loan_id)

        
        serializer = LoanSerializer(loan)

      
        response_data = {
            "loan_id": loan.id,
            "customer": serializer.data['customer'],  
            "loan_amount": serializer.data['loan_amount'],
            "interest_rate": serializer.data['interest_rate'],
            "monthly_installment": serializer.data['monthly_installment'],
            "tenure": serializer.data['tenure'],
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    





@api_view(['GET'])
def view_loans_by_customer(request, customer_id):
    try:
        # Fetch loans r
        loans = Loan.objects.filter(customer__id=customer_id)

        
        serializer = LoanSerializer(loans, many=True)

        response_data = []
        for loan_data in serializer.data:
            response_data.append({
                "loan_id": loan_data['id'],
                "loan_amount": loan_data['loan_amount'],
                "interest_rate": loan_data['interest_rate'],
                "monthly_installment": loan_data['monthly_installment'],
                "repayments_left": calculate_repayments_left(loan_data['tenure']), 
            })

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def calculate_repayments_left(tenure):
  
    return max(tenure - 6, 0)


def calculate_loan_credit_score(loan):

    try:
        emis_paid_on_time = loan.emis_paid_on_time
        tenure = loan.tenure

        if tenure == 0:
            raise ValueError("Tenure must be a non-zero positive integer")

       # ratio of EMIs paid on time to the total tenure
        credit_score = emis_paid_on_time / tenure

        return credit_score

    except Exception as e:
       
        raise e
