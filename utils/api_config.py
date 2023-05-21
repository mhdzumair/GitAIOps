import os


def get_api_token(service, request):
    """
    Return the API token for the given service.
    """
    if token := request.headers.get("Authorization"):
        api_token = token.lstrip("Bearer ")
    else:
        api_token = os.environ.get(f"{service}_TOKEN")

    if not api_token:
        raise RuntimeError(f"Missing {service}_TOKEN")
    return api_token
