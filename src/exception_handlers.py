import logging

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from .core.schemas.errors import ServerErrorSchema
from .core.schemas.validation import (
    BaseValidationErrorSchema,
    BaseValidationErrorsSchema,
)
from .exceptions.http.base import BaseFieldValidationHTTPException

log = logging.getLogger(__name__)


async def field_validation_exception_handler(
    _request: Request, exc: BaseFieldValidationHTTPException
) -> JSONResponse:
    content = BaseValidationErrorSchema(field=exc.field, detail=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseValidationErrorsSchema(
            errors=[content.model_dump()]
        ).model_dump(),
    )


async def pydantic_validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()
    formatted_errors = [
        BaseValidationErrorSchema(
            field=(
                error["loc"][1]
                if len(error["loc"]) > 1 and isinstance(error["loc"][1], str)
                else error["loc"][0]
            ),
            detail=error["msg"],
        ).model_dump()
        for error in errors
    ]
    return JSONResponse(
        status_code=422,
        content=BaseValidationErrorsSchema(
            errors=formatted_errors
        ).model_dump(),
    )


async def http_400_and_404_status_exception_handler(
    _request: Request, exc: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ServerErrorSchema(
            code=exc.status_code, detail=exc.detail
        ).model_dump(),
    )


def get_exception_handlers() -> dict:  # type: ignore[type-arg]
    return {
        BaseFieldValidationHTTPException: field_validation_exception_handler,
        RequestValidationError: pydantic_validation_exception_handler,
        status.HTTP_400_BAD_REQUEST: http_400_and_404_status_exception_handler,
        status.HTTP_404_NOT_FOUND: http_400_and_404_status_exception_handler,
    }
