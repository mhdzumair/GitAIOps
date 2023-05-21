import logging

from fastapi import APIRouter, HTTPException, Request
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError
from graphql import GraphQLError

from services.schemas import GraphQLQuery
from utils.api_config import get_api_token

router = APIRouter()
logging.getLogger("gql.transport.aiohttp").setLevel(logging.WARNING)


@router.post("/", operation_id="gitlab_graphql_api")
async def gitlab_graphql_api(request: Request, query: GraphQLQuery):
    """
    To execute a GraphQL query on the GitLab API, provide a GraphQLQuery object with the query string.
    The result will be the response from the GitLab API.
    """

    # Define the GraphQL transport
    transport = AIOHTTPTransport(
        url="https://gitlab.com/api/graphql",
        headers={
            "Content-type": "application/json",
            "PRIVATE-TOKEN": get_api_token("gitlab", request),
        },
    )

    # Create the GraphQL client
    async with Client(
        transport=transport,
        fetch_schema_from_transport=True,
    ) as session:
        # Define the GraphQL query
        gql_query = gql(query.query)

        # Execute the query
        try:
            result = await session.execute(gql_query)
        except TransportQueryError as error:
            raise HTTPException(
                status_code=400,
                detail=f"Error executing GraphQL query. failure reason: {error.errors}",
            )
        except GraphQLError as error:
            raise HTTPException(
                status_code=400,
                detail=f"Error executing GraphQL query. failure reason: {error.message}",
            )

    return result
