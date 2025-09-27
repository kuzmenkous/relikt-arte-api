from ..main import app
from .user import router as user_router

for router in (user_router,):
    app.include_router(router)
