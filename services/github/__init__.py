from fastapi import APIRouter
from .graphql import router as graphql_router
from .rest import router as rest_router

router = APIRouter()


router.include_router(graphql_router, prefix="/graphql")
router.include_router(rest_router, prefix="/rest")
