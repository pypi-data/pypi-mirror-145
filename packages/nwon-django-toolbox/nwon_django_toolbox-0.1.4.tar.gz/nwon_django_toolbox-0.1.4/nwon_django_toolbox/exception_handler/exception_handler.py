from rest_framework.views import exception_handler

from nwon_django_toolbox.exception_handler.get_error_message import get_error_message
from nwon_django_toolbox.exception_handler.get_response import get_response


def handle_exception(exc, context):
    error_response = exception_handler(exc, context)

    if error_response is not None:
        error = error_response.data

        if isinstance(error, list) and error:
            if isinstance(error[0], dict):
                error_response.data = get_response(
                    message=get_error_message(error[0]),
                    status_code=error_response.status_code,
                    result=error,
                )

            elif isinstance(error[0], str):
                error_response.data = get_response(
                    message=error[0],
                    status_code=error_response.status_code,
                    result=error,
                )

        if isinstance(error, dict):
            error_response.data = get_response(
                message=get_error_message(error),
                status_code=error_response.status_code,
                result=error,
            )
    return error_response
