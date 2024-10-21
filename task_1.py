# Mock imports - assume these modules are imported
import query_objects
import enums
from django.db import transaction
import update_object_in_database
import api_client

"""
Task: Restructure the following function for both robust functionality and maintainability.

The resulting return values in different scenarios should be constant.
* Code is pseudo code and does not have to run *
"""

def rest_endpoint(input):
    qs = query_objects(id=input.id)
    if not qs.exists():
        return 404
    obj = qs.get()
    if len(input.name) > 5:
        return 422
    obj.name = input.name + "_object"
    obj.save()
    if input.type != "bank_account":
        return 422
    obj.type = enums.Types.BANK_ACCOUNT
    obj.save()
    with transaction.atmoic():
        response = api_client.post(obj, input)
        if response.status != 200:
            return 500
        update_object_in_database(obj, input.details)
    return 200
