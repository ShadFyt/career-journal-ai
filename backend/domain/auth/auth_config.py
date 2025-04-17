import os
from datetime import timedelta

from authx import AuthX, AuthXConfig
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
ACCESS_TOKEN_EXPIRE_SECONDS = ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 1 day in seconds
REFRESH_TOKEN_EXPIRE_MINUTES = timedelta(days=20)  # 20 days

config = AuthXConfig(
    JWT_ALGORITHM=os.getenv("JWT_ALGORITHM"),
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1),
    JWT_COOKIE_MAX_AGE=ACCESS_TOKEN_EXPIRE_SECONDS,
    JWT_REFRESH_TOKEN_EXPIRES=REFRESH_TOKEN_EXPIRE_MINUTES,
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_SECURE=os.getenv("NODE_ENV") != "development",
)

security = AuthX(config)
