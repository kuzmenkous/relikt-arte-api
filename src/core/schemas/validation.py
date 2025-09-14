from pydantic import BaseModel


class BaseValidationErrorSchema(BaseModel):
    field: str
    detail: str


class BaseValidationErrorsSchema(BaseModel):
    errors: list[BaseValidationErrorSchema]
