import logging
import os


def get_api_token_header(service, request):
    """
    Return the API token for the given service.
    """
    if request.headers.get("Authorization"):
        return {"Authorization": request.headers.get("Authorization")}

    if private_token := os.environ.get(f"{service}_TOKEN"):
        return {"PRIVATE-TOKEN": private_token}

    raise RuntimeError(f"Missing {service}_TOKEN")
