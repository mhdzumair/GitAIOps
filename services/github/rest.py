import httpx
from fastapi import APIRouter, Request

from services.schemas import RestQuery
from utils.api_config import get_api_token_header

router = APIRouter()


@router.post("/", operation_id="github_rest_api")
async def github_rest_api(request: Request, query: RestQuery):
    """
    Make a REST API request to GitHub.
    Provide a RestQuery with endpoint, method, and optional data.
    The response will be JSON parsed as a dictionary or raw text.
    """

    github_api_url = "https://api.github.com"
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    headers.update(get_api_token_header("github", request))

    url = f"{github_api_url}/{query.endpoint}"

    async with httpx.AsyncClient() as client:
        if query.method.lower() == "get":
            response = await client.get(url, headers=headers)
        elif query.method.lower() == "post":
            response = await client.post(url, headers=headers, json=query.data)
        elif query.method.lower() == "put":
            response = await client.put(url, headers=headers, json=query.data)
        else:
            response = await client.delete(url, headers=headers)

    if "application/json" in response.headers.get("Content-Type", ""):
        return response.json()
    else:
        return response.text
