from core.exceptions import add_exception_handlers
from database.db import create_db_and_tables
from domain.technology.technology_router import router as technology_router
from fastapi import FastAPI

app = FastAPI()
add_exception_handlers(app)

# Register routers
app.include_router(technology_router, prefix="/api/technologies", tags=["technologies"])

if __name__ == "__main__":
    import uvicorn

    create_db_and_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)
