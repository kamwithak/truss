# Mock imports - assume these modules are imported
import IntegerField
import ForeignKey
import BooleanField
import DateTimeField, now
from django.db.models import OuterRef, Subquery, Max

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
    # Subquery to get the latest customer's id for each company
    latest_customer = Customer.objects.filter(
        company=OuterRef('pk')  # Match the company's primary key
    ).order_by('-created_at')  # Order by creation date, most recent first
    .values('id')[:1]  # Select only the id field and limit to 1 result

    # Query to get companies where the latest customer is a friend
    companies_with_recent_friend = Company.objects.annotate(
        # Add a field 'latest_customer_id' to each company
        latest_customer_id=Subquery(latest_customer)
    ).filter(
        # Match the customer's id with the latest_customer_id we just annotated
        customer__id=OuterRef('latest_customer_id'),
        customer__friend=True  # Ensure this customer is marked as a friend
    ).distinct()  # Remove any duplicate company entries

    # Convert QuerySet to list and return
    return list(companies_with_recent_friend)
