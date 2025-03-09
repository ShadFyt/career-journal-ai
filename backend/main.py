import contextlib

from core.admin.admin_portal import admin
from core.exceptions import add_exception_handlers
from database.db import create_db_and_tables
from domain.auth.auth_config import security
from domain.auth.auth_router import router as auth_router
from domain.journal_entry.journal_entry_router import router as journal_entry_router
from domain.project.project_router import router as project_router
from domain.technology.technology_router import router as technology_router
from domain.user.user_router import router as user_router
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
admin.mount_to(app)
security.handle_errors(app)


add_exception_handlers(app)

# Register routers
app.include_router(technology_router, prefix="/api/technologies", tags=["technologies"])
app.include_router(project_router, prefix="/api/projects", tags=["projects"])
app.include_router(
    journal_entry_router, prefix="/api/journal-entries", tags=["journal-entries"]
)
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
