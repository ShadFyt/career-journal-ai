from core.exceptions import add_exception_handlers
from database.db import create_db_and_tables
from domain.journal_entry.journal_entry_router import router as journal_entry_router
from domain.project.project_router import router as project_router
from domain.technology.technology_router import router as technology_router
from fastapi import FastAPI

app = FastAPI()
add_exception_handlers(app)

# Register routers
app.include_router(technology_router, prefix="/api/technologies", tags=["technologies"])
app.include_router(project_router, prefix="/api/projects", tags=["projects"])
app.include_router(journal_entry_router, prefix="/api/journal-entries", tags=["journal-entries"])

# @app.on_event("startup")
# async def on_startup():
#     await create_db_and_tables()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
