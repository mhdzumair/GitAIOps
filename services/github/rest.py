import json

import httpx
from fastapi import APIRouter, Request, HTTPException

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
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    headers.update(get_api_token_header("github", request))

    url = f"{github_api_url}/{query.endpoint}"

    if query.data:
        try:
            data = json.loads(query.data)
        except json.JSONDecodeError as error:
            raise HTTPException(
                status_code=400, detail=f"Error parsing JSON data. reason: {error}"
            )
    else:
        data = None

    async with httpx.AsyncClient() as client:
        if query.method.lower() == "get":
            response = await client.get(url, headers=headers, params=data)
        elif query.method.lower() == "post":
            response = await client.post(url, headers=headers, json=data)
        elif query.method.lower() == "put":
            response = await client.put(url, headers=headers, json=data)
        elif query.method.lower() == "patch":
            response = await client.patch(url, headers=headers, json=data)
        else:
            response = await client.delete(url, headers=headers, params=data)

    if "application/json" in response.headers.get("Content-Type", ""):
        return response.json()
    return response.text
