def get_error_message(error_dict: dict):
    field = next(iter(error_dict))
    response = error_dict[next(iter(error_dict))]

    if isinstance(response, dict):
        response = get_error_message(response)
    elif isinstance(response, list):
        response_message = response[0]
        if isinstance(response_message, dict):
            response = get_error_message(response_message)
        else:
            response = response[0]
    return response
