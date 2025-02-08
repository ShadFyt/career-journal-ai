from fastapi import FastAPI

from database.db import create_db_and_tables

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    create_db_and_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)
