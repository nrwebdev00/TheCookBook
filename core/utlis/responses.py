from rest_framework.response import Response

def standard_response(
    success: bool, 
    msg: str, 
    note: str="",  
    error_english: str="",
    error: dict=None,
    data: dict=None,
    status_code: int=200) -> Response:
    """
    Generate a standardized API response.

    Args:
        success (bool): Indicates if the request was successful.
        msg (str): A message describing the result.
        note (str, optional): Additional notes. Defaults to "".
        data (dict, optional): Additional data to include in the response. Defaults to None.
        status_code (int, optional): HTTP status code for the response. Defaults to 200.

    Returns:
        Response: A DRF Response object with the standardized format.
    """
    response_data = {
        "success": success,
        "msg": msg,
        "note": note,
        "error_english": error_english,
        "error": error if error is not None else {},
        "data": data if data is not None else {}
    }
    return Response(response_data, status=status_code)