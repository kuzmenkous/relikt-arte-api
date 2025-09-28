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
    formatted_errors = []

    for error in errors:
        if error["type"] == "union_tag_not_found":
            field = ".".join(str(part) for part in error["loc"])
            detail = (
                f"Field '{field}' is missing a required discriminator "
                f"{error['ctx'].get('discriminator', 'unknown')}. "
                "Please provide this field to determine the correct type."
            )
        elif error["type"] == "json_invalid":
            field = ".".join(str(part) for part in error["loc"])
            json_error = error["ctx"].get("error", "Invalid JSON")
            detail = (
                f"Invalid JSON at '{field}'. Error: {json_error}. "
                "Please check your JSON structure and try again."
            )
        else:
            field = error["loc"][-1] if len(error["loc"]) > 0 else "unknown"
            detail = error["msg"]

        formatted_errors.append(
            BaseValidationErrorSchema(field=field, detail=detail).model_dump()
        )

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
