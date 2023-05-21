from pydantic import BaseModel, validator


class GraphQLQuery(BaseModel):
    query: str


class RestQuery(BaseModel):
    endpoint: str
    method: str
    data: str = None

    @validator("method")
    def validate_method(cls, v):
        if v.lower() not in ["get", "post", "put", "delete", "patch"]:
            raise ValueError("Invalid method")
        return v
