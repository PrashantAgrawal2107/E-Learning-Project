from ..models.studentModel import Student
from fastapi import HTTPException, status

def sort_validation(valid_sort_fields, sort_by: str, order: str):
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort field. Allowed: {list(valid_sort_fields.keys())}"
        )
    
    if order.lower() not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order. Allowed: ['asc', 'desc']"
        )

    return valid_sort_fields[sort_by]