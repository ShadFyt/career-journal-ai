from fastapi import FastAPI
from domain.technology.router import router as technology_router
from database.db import create_db_and_tables

app = FastAPI()

# Register routers
app.include_router(technology_router, prefix="/api/technologies", tags=["technologies"])

if __name__ == "__main__":
    import uvicorn

    create_db_and_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)
