from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    per_page: int
    total_pages: int


class Diff(BaseModel):
    diff: str
    new_path: str
    old_path: str
    a_mode: str
    b_mode: str
    new_file: bool
    renamed_file: bool
    deleted_file: bool
    diff_pagination: Pagination


class MergeRequestDiffResponse(BaseModel):
    diffs: list[Diff]
    pagination: Pagination


class TraceLogResponse(BaseModel):
    trace_log: str
    pagination: Pagination
