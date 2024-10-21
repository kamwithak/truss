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

def validate_input(input):
    """
    Validate the input object for required fields and constraints.
    
    Args:
        input: The input object to validate.
    
    Returns:
        A tuple (error_message, status_code) if validation fails, (None, None) otherwise.
    """
    if not all([input.id, input.name, input.type, input.details]):
        return "Missing required fields", 400
    if len(input.name) > 5:
        return "Name too long", 422
    if input.type != "bank_account":
        return "Invalid type", 422
    return None, None

def fetch_object(id):
    """
    Fetch an object from the database using the given id.
    
    Args:
        id: The id of the object to fetch.
    
    Returns:
        A tuple (object, None) if the object is found, (None, error_tuple) otherwise.
    """
    try:
        return query_objects(id=id).get(), None
    except query_objects.DoesNotExist:
        return None, ("Object not found", 404)

def update_object(obj, input):
    """
    Update the given object with input data and perform associated operations.
    
    Args:
        obj: The object to update.
        input: The input data for the update.
    
    Returns:
        None if the update is successful, error message string otherwise.
    """
    obj.name = input.name + "_object"
    obj.type = enums.Types.BANK_ACCOUNT
    
    try:
        with transaction.atomic():
            obj.save()
            response = api_client.post(obj, input)
            if response.status != 200:
                raise Exception("API client error")
            update_object_in_database(obj, input.details)
        return None
    except Exception as e:
        return str(e)

def rest_endpoint(input):
    """
    Main REST endpoint function to handle input validation, object fetching, and updating.
    
    Args:
        input: The input data for the endpoint.
    
    Returns:
        JsonResponse with appropriate message and status code.
    """
    # Input validation
    error, status = validate_input(input)
    if error:
        return JsonResponse({"error": error}, status=status)

    # Fetch object
    obj, error = fetch_object(input.id)
    if error:
        return JsonResponse({"error": error[0]}, status=error[1])

    # Update object
    error = update_object(obj, input)
    if error:
        return JsonResponse({"error": error}, status=500)

    return JsonResponse({"message": "Success"}, status=200)
