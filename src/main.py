from fastapi import APIRouter, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import settings
from .core.schemas.errors import ServerErrorSchema
from .core.schemas.validation import BaseValidationErrorsSchema
from .exception_handlers import get_exception_handlers

# App configuration
app = FastAPI(
    title=settings.app.name,
    debug=settings.debug,
    version=str(settings.app.version),
    docs_url=settings.app.docs_url if settings.debug else None,
    redoc_url=settings.app.redoc_url if settings.debug else None,
    exception_handlers=get_exception_handlers(),
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": BaseValidationErrorsSchema,
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "errors": [
                            {"field": "field1", "detail": "error1"},
                            {"field": "field2", "detail": "error2"},
                        ]
                    }
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ServerErrorSchema,
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {"code": 400, "detail": "error"}
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ServerErrorSchema,
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {"code": 404, "detail": "Object not found"}
                }
            },
        },
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Mount static directory
app.mount(
    f"/{settings.static.dir}", StaticFiles(directory=settings.static.dir)
)

# Include routers
ROUTERS: list[APIRouter] = []
for router in ROUTERS:
    app.include_router(router, prefix=f"/api/v{settings.app.version}")
