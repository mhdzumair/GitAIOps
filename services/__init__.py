import os

from fastapi import APIRouter

services_router = APIRouter()
SERVICE_NAME = os.getenv("GITAIOPS_SERVICE_NAME", "gitlab")

if SERVICE_NAME == "gitlab":
    from services.gitlab import router as gitlab_router

    services_router.include_router(gitlab_router, tags=["GitLab"])

elif SERVICE_NAME == "github":
    from services.github import router as github_router

    services_router.include_router(github_router, tags=["GitHub"])
