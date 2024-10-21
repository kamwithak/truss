# Mock imports - assume these modules are imported
import IntegerField
import ForeignKey
import BooleanField
import DateTimeField, now

class Company(Model):
    structure = IntegerField()
class Customer(Model):
    created_at = DateTimeField(default=now)
    company = ForeignKey(Company)
    friend = BooleanField()

"""
Task: Implement this function using the Django models provided above.

Assume the function is part of the Django project which can access the data
using the Django ORM (database api).
* Code is pseudo code and does not have to run *
If you are unfamiliar with Django syntax already, pure pseudo code is fine
"""

def get_companies_with_recent_friend():
    """Get all companies where their most recently created customer is `friend=True`.

    Returns
    -------
    `list(Company, ...)`
    """
    # Get all companies
    companies = Company.objects.all()
    
    # List to store companies with recent friend
    result = []
    
    for company in companies:
        # Get the most recent customer for this company
        most_recent_customer = Customer.objects.filter(company=company).order_by('-created_at').first()
        
        # Check if the most recent customer is a friend
        if most_recent_customer and most_recent_customer.friend:
            result.append(company)
    
    return result
