import contextlib

from core.admin.admin_portal import admin
from core.exceptions import add_exception_handlers
from database.db import create_db_and_tables
from domain.auth.auth_config import security
from domain.auth.auth_dependencies import AuthDeps
from domain.auth.auth_router import router as auth_router
from domain.journal_entry.journal_entry_router import router as journal_entry_router
from domain.project.project_router import router as project_router
from domain.technology.technology_router import router as technology_router
from domain.user.user_router import router as user_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(
    title="Career Journal API",
    description="API for managing career journal",
    lifespan=lifespan,
    openapi_url="/api/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
)
admin.mount_to(app)
security.handle_errors(app)


add_exception_handlers(app)

# Register routers
app.include_router(
    technology_router,
    prefix="/api/technologies",
    tags=["technologies"],
    dependencies=[*AuthDeps],
)
app.include_router(
    project_router, prefix="/api/projects", tags=["projects"], dependencies=[*AuthDeps]
)
app.include_router(
    journal_entry_router,
    prefix="/api/journal-entries",
    tags=["journal-entries"],
    dependencies=[*AuthDeps],
)
app.include_router(
    user_router, prefix="/api/users", tags=["users"], dependencies=[*AuthDeps]
)
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
