import os

from fastapi import Request, HTTPException


def get_api_token_header(service: str, request: Request) -> dict:
    """
    Return the API token for the given service. If the server is local, it checks for the service token in the environment variables.
    If the server is not local, it expects the Authorization header in the request.

    Args:
        service (str): The name of the service (e.g., 'gitlab', 'github').
        request (Request): The incoming request object.

    Returns:
        dict: A dictionary containing the Authorization header.

    Raises:
        HTTPException: If the server is local and the service token is not found in the environment variables, or if the server is not local and the Authorization header is not found in the request.
    """
    if request.headers.get("Authorization"):
        return {"Authorization": request.headers.get("Authorization")}

    if "localhost" in str(request.base_url) or "127.0.0.1" in str(request.base_url):
        if private_token := os.environ.get(f"{service.upper()}_TOKEN"):
            return {"Authorization": f"Bearer {private_token}"}
        raise HTTPException(
            status_code=401,
            detail=f"Missing {service.upper()}_TOKEN in environment variables",
        )
    raise HTTPException(
        status_code=401, detail="Missing Authorization header in the request"
    )
