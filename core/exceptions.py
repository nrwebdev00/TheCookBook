from rest_framework.views import exception_handler
from core.utlis.responses import standard_response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return standard_response(
            success=False,
            msg="",
            note="",
            error_english=str(exc),
            error=responses.data,
            data=None,
            status_code=response.status_code
        )
        
    return standard_response(
        success=False,
        msg="",
        note="",
        error_english=str(exc),
        error=None,
        data=None,
        status_code=500
    )   