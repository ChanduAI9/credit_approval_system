from decimal import Decimal

def calculate_approved_limit(monthly_salary):
  
    return round(36 * monthly_salary, -5)

def calculate_loan_credit_score(loan):
   
    return loan.emis_paid_on_time / loan.tenure

def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
   

    if interest_rate is not None:
        monthly_installment = calculate_monthly_installment(float(loan_amount), float(interest_rate), int(tenure))
        return True, Decimal(interest_rate), Decimal(monthly_installment)

    return False, None, None

def calculate_monthly_installment(loan_amount, interest_rate, tenure):
    

    if interest_rate is None:
        raise ValueError("Interest rate cannot be None")

    if tenure is None or tenure == 0:
        raise ValueError("Tenure must be a non-zero positive integer")

    try:
        interest_rate = Decimal(interest_rate)  
    except (TypeError, ValueError):
        raise ValueError("Invalid interest rate value")

    interest_rate /= 100  #  percentage to decimal

    monthly_rate = interest_rate / 12
    num_installments = tenure * 12
    monthly_installment = (loan_amount * monthly_rate) / (1 - (1 + monthly_rate) ** -num_installments)

    return monthly_installment
