from typing import List

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    status: str = 'success'
    data: dict = Field(default={})


class ErrorResponse(BaseModel):
    status: str = 'fail'
    message: str = Field()
    errors: dict | List[dict | str] = Field(default={})
