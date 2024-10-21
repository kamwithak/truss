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
    raise NotImplementedError
