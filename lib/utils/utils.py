from typing import Any, Dict, Optional, Tuple

def error_response(status_code: int, message: str, details: Optional[Any] = None) -> Tuple[Dict[str, Any], int]:
    payload: Dict[str, Any] = {
        "error": {
            "code": status_code,
            "message": message
        }
    }
    if details is not None:
        payload["error"]["details"] = details
    return payload, status_code
