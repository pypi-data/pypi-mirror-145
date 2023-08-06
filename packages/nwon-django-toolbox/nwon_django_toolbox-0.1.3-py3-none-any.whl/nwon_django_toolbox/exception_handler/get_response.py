from typing import List, Union


def get_response(
    message: str = "",
    result: Union[dict, List, None] = None,
    status_code: int = 200,
):
    return {
        "message": message,
        "result": result,
        "status_code": status_code,
    }
