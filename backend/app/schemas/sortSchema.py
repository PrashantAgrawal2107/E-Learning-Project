from pydantic import BaseModel

class SortSchema(BaseModel):
    sort_by: str = "created_on"
    order: str = "asc"
    skip: int = 0
    limit: int = 10