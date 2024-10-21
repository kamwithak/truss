# Mock imports - assume these modules are imported
import query_objects
import enums
from django.db import transaction
import update_object_in_database
import api_client
from django.http import JsonResponse

"""
Task: Restructure the following function for both robust functionality and maintainability.

The resulting return values in different scenarios should be constant.
* Code is pseudo code and does not have to run *
"""

def rest_endpoint(input):
    # Input validation
    if not input.id or not input.name or not input.type or not input.details:
        return JsonResponse({"error": "Missing required fields"}, status=400)

    if len(input.name) > 5:
        return JsonResponse({"error": "Name too long"}, status=422)

    if input.type != "bank_account":
        return JsonResponse({"error": "Invalid type"}, status=422)

    # Fetch object
    try:
        obj = query_objects(id=input.id).get()
    except query_objects.DoesNotExist:
        return JsonResponse({"error": "Object not found"}, status=404)

    # Update object
    obj.name = input.name + "_object"
    obj.type = enums.Types.BANK_ACCOUNT

    try:
        with transaction.atomic():
            obj.save()
            response = api_client.post(obj, input)
            if response.status != 200:
                raise Exception("API client error")
            update_object_in_database(obj, input.details)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Success"}, status=200)
