import json

import httpx
from fastapi import APIRouter, HTTPException, Request

from services.schemas import RestQuery
from utils.api_config import get_api_token_header

router = APIRouter()
gitlab_api_url = "https://gitlab.com/api/v4"


@router.post("/", operation_id="gitlab_rest_api")
async def gitlab_rest_api(request: Request, query: RestQuery):
    """
    Make a REST API request to GitLab.
    Provide a RestQuery with endpoint, method, and optional data.
    The response will be JSON parsed as a dictionary or raw text.
    """

    if query.data:
        try:
            data = json.loads(query.data)
        except json.JSONDecodeError as error:
            raise HTTPException(
                status_code=400, detail=f"Error parsing JSON data. reason: {error}"
            )
    else:
        data = None

    # Define the full URL for the request
    url = f"{gitlab_api_url}/{query.endpoint.lstrip('/')}"
    headers = {
        "Content-Type": "application/json",
    }
    headers.update(get_api_token_header("gitlab", request))

    # Send the request and get the response
    async with httpx.AsyncClient() as client:
        try:
            if query.method.lower() == "get":
                response = await client.get(url, headers=headers, params=data)
            elif query.method.lower() == "post":
                response = await client.post(url, headers=headers, json=data)
            elif query.method.lower() == "put":
                response = await client.put(url, headers=headers, json=data)
            else:
                response = await client.delete(url, headers=headers, params=data)

            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=f"{e.response.text}"
            )

    # Check the Content-Type of the response
    if "application/json" in response.headers.get("Content-Type", ""):
        data = response.json()
    else:
        data = response.text

    return data
