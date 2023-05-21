from urllib.parse import quote_plus

import httpx
from fastapi import APIRouter, HTTPException, Request

from services.gitlab.schemas import MergeRequestDiffResponse, TraceLogResponse
from utils.api_config import get_api_token_header
from utils.log_scrubber import scrub_log
from utils.paginator import paginate_content

router = APIRouter()
gitlab_api_url = "https://gitlab.com/api/v4"


@router.get(
    "/jobs/trace", response_model=TraceLogResponse, operation_id="gitlab_trace_log"
)
async def gitlab_trace_log(
    request: Request, project_id: str, job_id: str, page: int = 1, per_page: int = 8000
):
    """
    To retrieve the trace log for a specific job in a GitLab project,
    provide the project ID and job ID. also specify the page number and number of characters per page for pagination.
    The response will include the trace log and pagination details.
    """

    url = f"{gitlab_api_url}/projects/{quote_plus(project_id)}/jobs/{job_id}/trace"

    headers = {
        "Content-Type": "application/json",
    }
    headers.update(get_api_token_header("gitlab", request))

    # Send the request and get the response
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=f"{e.response.text}"
            )

    # Get the raw text of the response
    data = response.text
    paginated_data, pagination_detail = paginate_content(data, page, per_page)
    scrubbed_data = scrub_log(paginated_data)

    # Prepare the response
    response_data = {"trace_log": scrubbed_data, "pagination": pagination_detail}

    return response_data


@router.get(
    "/merge_requests/diff",
    response_model=MergeRequestDiffResponse,
    operation_id="gitlab_merge_request_diff",
)
async def gitlab_merge_request_diff(
    request: Request,
    project_id: str,
    merge_request_id: str,
    page: int = 1,
    per_page: int = 1,
    diff_page: int = 1,
    diff_per_page: int = 6000,
):
    """
    Get a merge request's diff in a GitLab project.
    Provide project ID and merge request ID.
    You can also specify the page number and number of change files per page for pagination,
    as well as the diff page number and number of diff characters per page for diff content pagination.
    """

    url = f"{gitlab_api_url}/projects/{quote_plus(project_id)}/merge_requests/{merge_request_id}/diffs"
    headers = {
        "Content-Type": "application/json",
    }
    headers.update(get_api_token_header("gitlab", request))

    # Send the request and get the response
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url, headers=headers, params={"page": page, "per_page": per_page}
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=f"{e.response.text}"
            )

    diffs = response.json()

    # Paginate the diff of each file
    for diff in diffs:
        paginated_diff, pagination_detail = paginate_content(
            diff["diff"], diff_page, diff_per_page
        )
        diff["diff"] = paginated_diff
        diff["diff_pagination"] = pagination_detail

    # Get GitLab pagination details from the headers
    gitlab_pagination = {
        "page": response.headers.get("X-Page"),
        "per_page": response.headers.get("X-Per-Page"),
        "total_pages": response.headers.get("X-Total-Pages"),
    }

    return {"diffs": diffs, "pagination": gitlab_pagination}
